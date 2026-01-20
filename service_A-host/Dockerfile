# Service A - Host Service (gRPC Server + FastAPI)
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
# Copy requirements from parent directory during build
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy service_A-host files
COPY service_A-host/ .

# Expose ports
# 50051 for gRPC
# 8000 for FastAPI
EXPOSE 50051 8000

# Run the FastAPI server (which also starts gRPC server in background)
CMD ["python", "fastapi_server.py"]
