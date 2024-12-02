import os
from pathlib import Path
from flask import Flask, request, render_template, jsonify
from werkzeug.utils import secure_filename
from raglite import RAGLiteConfig, insert_document, rag, hybrid_search, retrieve_chunks, rerank
from rerankers import Reranker

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER', '/app/uploads')
app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_CONTENT_LENGTH', 16777216))

# Set Ollama API base URL
os.environ["OLLAMA_API_BASE"] = "http://ollama:11434"

def get_raglite_config():
    return RAGLiteConfig(
        db_url=os.getenv('DATABASE_URL', 'sqlite:///data/raglite.sqlite'),
        llm="ollama/llama2",
        embedder="text-embedding-3-small",
        reranker=(
            ("en", Reranker("ms-marco-MiniLM-L-12-v2", model_type="flashrank")),
            ("other", Reranker("ms-marco-MultiBERT-L-12", model_type="flashrank"))
        )
    )

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'files[]' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    files = request.files.getlist('files[]')
    processed_files = []
    
    config = get_raglite_config()
    
    for file in files:
        if file.filename == '':
            continue
            
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            # Check for database in the new location
            if not os.path.exists('/app/data/raglite.sqlite'):
                insert_document(Path(filepath), config=config)
                processed_files.append(filename)
            else:
                processed_files.append(f"{filename} (using existing database)")
        except Exception as e:
            return jsonify({'error': f'Error processing {filename}: {str(e)}'}), 500
    
    return jsonify({'success': True, 'processed_files': processed_files})

@app.route('/query', methods=['POST'])
def process_query():
    query = request.form.get('query')
    if not query:
        return jsonify({'error': 'No query provided'}), 400
    
    config = get_raglite_config()
    
    try:
        # Using the exact same code structure from your working script
        chunk_ids, *_ = hybrid_search(query, num_results=5, config=config)
        chunks = retrieve_chunks(chunk_ids, config=config)
        reranked_chunks = rerank(query, chunks, config=config)
        
        response = ""
        for update in rag(query, search=reranked_chunks, config=config):
            response += update
            
        return jsonify({'success': True, 'response': response})
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        return jsonify({'error': str(e), 'details': error_details}), 500

if __name__ == '__main__':
    # Set OpenAI API key from environment variable
    if "OPENAI_API_KEY" not in os.environ:
        raise ValueError("OPENAI_API_KEY environment variable must be set")
        
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(host='0.0.0.0', port=5454)