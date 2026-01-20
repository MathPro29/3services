# Service B - gRPC Client
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy service_B files
COPY service_B/ .

# Run the gRPC client
CMD ["python", "main.py"]
