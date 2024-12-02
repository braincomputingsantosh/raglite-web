FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create necessary directories
RUN mkdir -p /app/templates /app/static /app/uploads /app/data /app/.flashrank_cache

# Copy requirements first for better caching
COPY ./requirements.txt .
RUN pip install --no-cache-dir "numpy<2.0.0" && \
    pip install --no-cache-dir -r requirements.txt && \
    python -m spacy download xx_sent_ud_sm

# Copy files individually
COPY ./app.py /app/
COPY ./templates/index.html /app/templates/
COPY ./static/styles.css /app/static/

# Set permissions
RUN chown -R 1000:1000 /app && \
    chmod -R 755 /app && \
    chmod -R 777 /app/uploads /app/data /app/.flashrank_cache

# Document that the container listens on port 5454
EXPOSE 5454

# Command to run the application
CMD ["python", "app.py"]