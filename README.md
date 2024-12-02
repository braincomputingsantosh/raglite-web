# RAGLite Web Application

A web-based interface for document processing and querying using RAGLite, Ollama, and OpenAI. This application allows users to upload documents and ask questions about their content using a combination of local and cloud-based AI models.

## Project Structure
```
raglite-web/
├── app/
│   ├── Dockerfile
│   ├── app.py
│   ├── requirements.txt
│   ├── static/
│   │   └── styles.css
│   ├── templates/
│   │   └── index.html
│   └── uploads/
├── ollama/
│   ├── Dockerfile
│   └── init.sh
├── docker-compose.yml
└── .env
```

## Raglite:
https://github.com/superlinear-ai/raglite


## Prerequisites
- Docker and Docker Compose
- OpenAI API key

## Setup Instructions

1. Clone the repository:
```bash
git clone <repository-url>
cd raglite-web
```

2. Create the required directories:
```bash
mkdir -p app/uploads app/static app/templates app/data
```

3. Create a `.env` file in the root directory:
```bash
echo "OPENAI_API_KEY=your-openai-api-key-here" > .env
```

4. Build and start the services:
```bash
docker-compose up --build
```

The application will be available at http://localhost:5454

## Features
- Document upload support for various formats (PDF, TXT, DOC, DOCX)
- Real-time document processing using RAGLite
- Question-answering capabilities using Ollama's llama2 model
- Progress indicators for uploads and queries
- Persistent storage for uploaded documents and database

## Components
- **Web Interface**: Flask-based web application
- **RAGLite**: Document processing and retrieval
- **Ollama**: Local LLM server (llama2 model)
- **OpenAI**: Text embeddings (text-embedding-3-small)

## Usage
1. Access the web interface at http://localhost:5454
2. Upload documents using the file upload interface
3. Enter queries in the text area and submit
4. View responses generated from your documents

## Docker Services
- **web**: Flask application for the web interface
- **ollama**: Local LLM server running llama2

## Environment Variables
- `OPENAI_API_KEY`: Your OpenAI API key
- `OLLAMA_API_BASE`: URL for Ollama server (set automatically)
- `DATABASE_URL`: SQLite database path (set automatically)

## Development
To modify the application:
1. Edit files in the appropriate directories
2. Rebuild and restart services:
```bash
docker-compose down
docker-compose up --build
```

## Troubleshooting
1. If uploads fail, check:
   - Directory permissions in app/uploads
   - Available disk space
   - File size limits

2. If queries fail, verify:
   - Ollama service is running
   - llama2 model is downloaded
   - OpenAI API key is valid

3. For database issues:
   - Check permissions on app/data directory
   - Verify SQLite database file permissions

## Notes
- The application uses SQLite for document storage
- Uploaded documents are processed once and stored in the database
- The llama2 model is downloaded automatically on first startup

## How to use?

1. Instead of an open-ended "Tell me about this document", try specific questions like:
- "What are the main conclusions of this paper?"
- "What is the methodology used in this research?"
- "What are the key findings about [specific topic] in this document?"

2. For technical documents:
- "Can you explain the concept of [specific term] mentioned in the document?"
- "What are the prerequisites discussed in section [X]?"
- "How does this paper define [specific concept]?"

3. For research papers:
- "What problem is this research trying to solve?"
- "What are the limitations of this study?"
- "How does this paper compare to previous work in the field?"

4. For error resolution:
Let's try a simple, concrete question to test if the RAG system is working. Try this:
"What is the main topic discussed in this document?"


## Screen shot:

![Screenshot 2024-12-02 at 2 12 46 PM](https://github.com/user-attachments/assets/c5419137-29cb-46c9-8723-a19b669ba35f)
