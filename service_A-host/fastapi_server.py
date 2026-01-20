from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from threading import Thread
from grpc_server import serve as grpc_serve

# Mock database - แก้ไขข้อมูลตรงนี้ (ต้องเหมือนกับใน grpc_server.py)
USERS_DB = {
    1: "Alice",
    2: "Bob",
    3: "Charlie",
    4: "David",
    5: "Eve",
    10: "Admin",
    99: "Guest",
    100: "Anonymous"
}

# FastAPI app
app = FastAPI(
    title="User Service API",
    description="gRPC User Service with REST API interface",
    version="1.0.0"
)

# Pydantic models for request/response
class UserRequest(BaseModel):
    id: int

class UserResponse(BaseModel):
    id: int
    name: str

@app.get("/")
def read_root():
    """Root endpoint"""
    return {
        "message": "User Service API",
        "docs": "/docs",
        "grpc_port": 50051,
        "rest_port": 8000,
        "available_users": list(USERS_DB.keys())
    }

@app.get("/users")
def get_all_users():
    """Get all users"""
    return {
        "total": len(USERS_DB),
        "users": [{"id": uid, "name": name} for uid, name in USERS_DB.items()]
    }

@app.get("/user/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    """Get user by ID"""
    if user_id <= 0:
        raise HTTPException(status_code=400, detail="User ID must be positive")
    
    # ค้นหา user จาก database
    user_name = USERS_DB.get(user_id)
    
    if user_name is None:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")
    
    return UserResponse(id=user_id, name=user_name)

@app.post("/user", response_model=UserResponse)
def get_user_post(request: UserRequest):
    """Get user by ID (POST method)"""
    if request.id <= 0:
        raise HTTPException(status_code=400, detail="User ID must be positive")
    
    # ค้นหา user จาก database
    user_name = USERS_DB.get(request.id)
    
    if user_name is None:
        raise HTTPException(status_code=404, detail=f"User with ID {request.id} not found")
    
    return UserResponse(id=request.id, name=user_name)

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "user-service"}

def run_grpc_server():
    """Run gRPC server in background thread"""
    print("Starting gRPC server on port 50051...")
    grpc_serve()

if __name__ == "__main__":
    # Start gRPC server in background thread
    grpc_thread = Thread(target=run_grpc_server, daemon=True)
    grpc_thread.start()
    
    # Start FastAPI server
    print("Starting FastAPI server on port 8000...")
    print("Swagger UI available at: http://localhost:8000/docs")
    print("ReDoc available at: http://localhost:8000/redoc")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
