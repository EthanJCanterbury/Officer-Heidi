
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install uv package manager
RUN pip install uv

# Install Python dependencies
RUN uv sync --frozen

# Copy application code
COPY . .

# Expose port 5000
EXPOSE 5000

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV FLASK_ENV=production

# Run the application
CMD ["python", "main.py"]
