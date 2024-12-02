#!/bin/sh

# Start Ollama server
ollama serve &

# Wait for Ollama to be ready
echo "Waiting for Ollama to start..."
until curl -s -f http://localhost:11434 > /dev/null 2>&1; do
    sleep 1
done

echo "Pulling llama2 model..."
ollama pull llama2

# Keep container running
tail -f /dev/null