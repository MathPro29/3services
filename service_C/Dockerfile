# Service C - REST Client
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy service_C files
COPY service_C/ .

# Run the REST client
CMD ["python", "main.py"]
