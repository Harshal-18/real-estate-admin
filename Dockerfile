FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create uploads directory
RUN mkdir -p /app/app/static/uploads

# Set proper permissions
RUN chmod -R 755 /app/app/static/uploads
RUN chmod +x /app/start.sh

EXPOSE 5000

# Use the startup script
CMD ["python", "run.py"] 