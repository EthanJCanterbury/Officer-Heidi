
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency files first
COPY pyproject.toml ./

# Install uv package manager
RUN pip install uv

# Create a simple requirements.txt from pyproject.toml for better compatibility
RUN echo "slack-bolt>=1.18.0" > requirements.txt && \
    echo "GitPython>=3.1.0" >> requirements.txt && \
    echo "requests>=2.31.0" >> requirements.txt && \
    echo "websocket-client>=1.6.0" >> requirements.txt && \
    echo "flask>=3.1.1" >> requirements.txt

# Install Python dependencies using pip for better compatibility
RUN pip install -r requirements.txt

# Copy application code
COPY . .

# Create a non-root user for security
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose port 5000
EXPOSE 5000

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV FLASK_ENV=production

# Run the application
CMD ["python", "main.py"]
