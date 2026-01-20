

import grpc
from concurrent import futures
import user_pb2
import user_pb2_grpc

# ===== MOCK DATABASE =====
# Database จำลองสำหรับเก็บข้อมูล user
# Key = User ID (int), Value = User Name (string)
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

# ===== USER SERVICE CLASS =====
# Class นี้ implement gRPC service ตาม proto/user.proto
class UserService(user_pb2_grpc.UserServiceServicer):
    """
    UserService: สำหรับจัดการข้อมูล User
    
    Methods:
        GetUser(request, context) -> UserReply
            - รับ UserRequest ที่มี id
            - ค้นหา user จาก USERS_DB
            - ส่งกลับ UserReply ที่มี id และ name
    """
    
    def GetUser(self, request, context):
        """
        GetUser Method
        
        Request (จาก Service B):
            UserRequest {
                int32 id = 1;  // User ID ที่ต้องการค้นหา
            }
        
         Response (ส่งกลับไป Service B):
            UserReply {
                int32 id = 1;      // User ID
                string name = 2;   // User Name
            }
        """
        
        # ค้นหา user จาก database โดยใช้ id จาก request
        user_name = USERS_DB.get(request.id)
        
        if user_name is None:
            # กรณีไม่เจอ user ใน database
            # ส่ง gRPC error กลับไป
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f'User with ID {request.id} not found')
            return user_pb2.UserReply()  # Return empty reply
        
        # กรณีเจอ user ใน database
        # สร้าง UserReply และส่งกลับไป
        return user_pb2.UserReply(
            id=request.id,      # User ID ที่ค้นหา
            name=user_name      # User Name จาก database
        )

# ===== SERVER STARTUP FUNCTION =====
def serve():
    """
    ฟังก์ชันสำหรับ gRPC Server
    
    Configuration:
        - Max workers: 10 (จำนวน thread สำหรับรับ request พร้อมกัน)
        - Port: 50051
        - Protocol: gRPC (insecure - ไม่มี SSL/TLS)
    
    Process:
        1. สร้าง gRPC server
        2. Register UserService
        3. Bind กับ port 50051
        4. Start server
        5. รอรับ request (blocking)
    """
    
    # สร้าง gRPC server พร้อม ThreadPoolExecutor
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    
    # Register UserService กับ server
    user_pb2_grpc.add_UserServiceServicer_to_server(
        UserService(), server
    )
    
    # Bind server กับ port 50051 (รับ connection จากทุก IP)
    server.add_insecure_port("[::]:50051")
    
    # แสดงข้อความว่า server เริ่มทำงานแล้ว
    print("gRPC Server started on port 50051")
    print(f"Available users: {list(USERS_DB.keys())}")
    
    # เริ่ม server
    server.start()
    
    # รอรับ request (blocking - จะไม่จบจนกว่าจะ terminate)
    server.wait_for_termination()
