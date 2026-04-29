# ─────────────────────────────────────────
#  ACEest Fitness & Gym - Dockerfile
#  Version: 3.2.4
# ─────────────────────────────────────────

# Base image - lightweight Python
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=app.py \
    FLASK_ENV=production

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for Docker cache optimization)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all application files
COPY app.py .
COPY templates/ templates/

# Create directory for SQLite database
RUN mkdir -p /app/data

# Expose port 5000
EXPOSE 5000

# Health check for Kubernetes
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')"

# Run the application
CMD ["python", "app.py"]
