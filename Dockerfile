# Base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install dependencies for OpenCV (OpenGL libraries)
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    && rm -rf /var/lib/apt/lists/*

# Install opencv-python-headless and other Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app source code
COPY . .

# Expose port (if needed, for FastAPI or others)
EXPOSE 8000

# Run the main script
CMD ["python3", "main.py"]