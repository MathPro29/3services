import grpc
import user_pb2
import user_pb2_grpc
import os

def get_user():
    """
    ฟังก์ชันสำหรับเรียก GetUser จาก Service A ผ่าน gRPC
    
    Configuration:
        - ใช้ environment variable GRPC_SERVER
        - Default: localhost:50051 (สำหรับรันแบบ local)
        - Docker: service_a:50051 (ตั้งค่าใน docker-compose.yml)
    
    Request ที่ส่งไป Service A:
        UserRequest {
            int32 id = 1;  // ขอข้อมูล user ID 1
        }
    
    Response ที่ได้รับจาก Service A:
        UserReply {
            int32 id = 1;
            string name = "Alice";
        }
    
   
    """
    
    # อ่าน gRPC server address จาก environment variable
    # ถ้าไม่มีให้ใช้ localhost:50051 (สำหรับรันแบบ local)
    grpc_server = os.getenv("GRPC_SERVER", "localhost:50051")
    
    try:
        # ===== STEP 1: สร้าง gRPC Channel =====
        # Channel คือ connection ไปยัง gRPC server
        channel = grpc.insecure_channel(grpc_server)
        
        # ===== STEP 2: สร้าง Stub =====
        # Stub คือ client object ที่ใช้เรียก remote methods
        stub = user_pb2_grpc.UserServiceStub(channel)
        
        # ===== STEP 3: เรียก GetUser Method =====
        # ส่ง UserRequest(id=1) ไปยัง Service A
        response = stub.GetUser(user_pb2.UserRequest(id=1))
        
        # ===== STEP 4: แสดงผลลัพธ์ =====
        print(f"✅ Success: id={response.id}, name={response.name}")
        return response
        
    except grpc.RpcError as e:
        # กรณีเกิด error จาก gRPC (เช่น connection failed, NOT_FOUND)
        print(f"❌ gRPC Error: {e.details()}")
        print(f"Make sure gRPC server is running at {grpc_server}")
