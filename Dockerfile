# Dockerfile for Manim AI Studio
# This image includes all dependencies for Manim rendering

FROM python:3.11-slim

# Install system dependencies for Manim
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    texlive-latex-base \
    texlive-fonts-recommended \
    texlive-fonts-extra \
    texlive-latex-extra \
    libcairo2-dev \
    libpango1.0-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create workspace directory
RUN mkdir -p workspace

# Expose port
EXPOSE 5001

# Environment variables
ENV PORT=5001
ENV PYTHONUNBUFFERED=1

# Run the server
CMD ["python", "api/server.py"]
