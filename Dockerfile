
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency files first
COPY pyproject.toml ./

# Install Python dependencies directly from pyproject.toml
RUN pip install --no-cache-dir \
    slack-bolt>=1.18.0 \
    GitPython>=3.1.0 \
    requests>=2.31.0 \
    websocket-client>=1.6.0 \
    flask>=3.1.1

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
ENV PYTHONPATH=/app

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl -f http://127.0.0.1:5000/webhook/health || exit 1

# Run the application
CMD ["python", "main.py"]
