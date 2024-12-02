FROM ollama/ollama:latest

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Copy initialization script
COPY init.sh /init.sh
RUN chmod +x /init.sh

# Set the entrypoint to our initialization script
ENTRYPOINT ["/init.sh"]