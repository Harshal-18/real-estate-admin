FROM python:3.10-slim

# Install system dependencies including PostgreSQL client
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    postgresql-client \
    build-essential \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

# Copy application code
COPY . .

# Create uploads directory
RUN mkdir -p /app/app/static/uploads

# Set proper permissions
RUN chmod -R 755 /app/app/static/uploads
RUN chmod +x /app/start.sh

EXPOSE 5000

# Use gunicorn for production
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "run:app"] 