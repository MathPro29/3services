from fastapi_server import app
import uvicorn
from threading import Thread
from grpc_server import serve as grpc_serve

def run_grpc_server():
    """Run gRPC server in background thread"""
    print(" Starting gRPC server on port 50051...")
    grpc_serve()

if __name__ == "__main__":
    # Start gRPC server in background thread
    grpc_thread = Thread(target=run_grpc_server, daemon=True)
    grpc_thread.start()
    
    # Start FastAPI server
    print(" Starting FastAPI server on port 8000...")
    print(" Swagger UI: http://localhost:8000/docs")
    print(" ReDoc: http://localhost:8000/redoc")
    print(" API endpoints:")
    print("   - GET  http://localhost:8000/")
    print("   - GET  http://localhost:8000/user/{user_id}")
    print("   - POST http://localhost:8000/user")
    print("   - GET  http://localhost:8000/health")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
