                    โปรเจค FastAPI Microservices
                    6604101371 เมธัส พรวิสุทธิ์

=======================================================
โปรเจคนี้เป็นระบบ Microservices ที่ประกอบด้วย 3 services หลัก:
- Service A: Host Service (มีทั้ง gRPC Server และ FastAPI Server)
- Service B: gRPC Client (เชื่อมต่อกับ Service A ผ่าน gRPC)
- Service C: REST Client (เชื่อมต่อกับ Service A ผ่าน REST API)


 (Project Tree)

methat371/
├── service_A-host/          # Service A - เป็น HOST
│   ├── Dockerfile           # Docker
│   ├── main.py              # Entry point สำหรับรัน gRPC server
│   ├── grpc_server.py       # gRPC Server
│   ├── fastapi_server.py    # FastAPI Server
│   ├── main_fastapi.py      # Entry point สำหรับรันทั้ง gRPC + FastAPI
│   ├── proto/
│   │   └── user.proto       # Protocol Buffer
│   ├── user_pb2.py          # ไฟล์หลังจาก Generate
│   └── user_pb2_grpc.py     # ไฟล์หลังจาก Generate
│
├── service_B/               # Service B - gRPC Client
│   ├── Dockerfile           # Docker
│   ├── main.py              # Entry point สำหรับรัน gRPC client
│   ├── grpc_client.py       # gRPC Client
│   ├── test_grpc.py         # gRPC testing script (ทดสอบหลาย user)
│   ├── proto/
│   │   └── user.proto       # Protocol Buffer
│   ├── user_pb2.py          # ไฟล์หลังจาก Generate
│   └── user_pb2_grpc.py     # ไฟล์หลังจาก Generate
│
├── service_C/               # Service C - REST Client
│   ├── Dockerfile           # Docker
│   ├── main.py              # Entry point สำหรับรัน REST client
│   └── rest_client.py       # REST API Client
│
├── docker-compose.yml       # Docker
├── requirements.txt         # Python dependencies
├── .dockerignore           # ไฟล์ที่ไม่ต้อง copy เข้า Docker
└── README.txt              # ไฟล์นี้


การทำงาน

   Service A เป็น Host Service ที่มี 2 servers ทำงานพร้อมกัน:
   1. gRPC Server (port 50051) - รับ request จาก Service B
   2. FastAPI Server (port 8000) - รับ request จาก Service C

1. grpc_server.py
      - gRPC Server implementation
      - ให้ร GetUser(UserRequest) -> UserReply
      - ค้นหาข้อมูล user จาก USERS_DB (จาก Mockup)
    ส่ง :
      Request:  UserRequest { id: 1 }
    ผลลัพธ์ :
      Response: UserReply { id: 1, name: "Alice" }
      
2. fastapi_server.py
      - FastAPI Server implementation
      - ให้ REST API endpoints
      - ใช้ USERS_DB เดียวกันกับ gRPC Server (จาก Mockup)
    ส่ง :
      Request:  GET /user/1
    ผลลัพธ์ :
      Response: {"id": 1, "name": "Alice"}
      
3. main_fastapi.py
      - รัน gRPC Server ใน background thread
      - รัน FastAPI Server ใน main thread
      - ทำให้ทั้ง 2 servers ทำงานพร้อมกัน

วิธีการรัน:
   รันทั้ง gRPC และ FastAPI พร้อมกัน
   python service_A-host\main_fastapi.py
   
   หรือรันแยก
   python service_A-host\grpc_server.py      # gRPC
   python service_A-host\fastapi_server.py   # FastAPI


  ***  Service B เป็น gRPC Client ที่เชื่อมต่อกับ Service A ***
   เพื่อดึงข้อมูล user ผ่าน gRPC protocol

    1. grpc_client.py
      - gRPC Client implementation
      - สร้าง gRPC channel ไปยัง Service A (port 50051)
      - เรียก GetUser(id=1) จาก Service A
      
   2. test_grpc.py
      - ทดสอบ gRPC client กับ user หลายคน
      - ทดสอบทั้ง success case และ error case
      - แสดงผลลัพธ์แบบละเอียด
   วิธีการรัน:
      python service_B\test_grpc.py   
      python service_B\grpc_client.py
    ผลลัพธ์:
    ==================================================
🧪 Testing gRPC GetUser
==================================================

📋 Testing existing users:
✅ User ID 1: Alice
✅ User ID 2: Bob
✅ User ID 3: Charlie
✅ User ID 4: David
✅ User ID 5: Eve
✅ User ID 10: Admin
✅ User ID 99: Guest
✅ User ID 100: Anonymous

📋 Testing non-existent users:
❌ User ID 999: User with ID 999 not found
❌ User ID 0: User with ID 0 not found
❌ User ID -1: User with ID -1 not found

==================================================
✅ Test completed!
==================================================

   *** Service C เป็น REST API Client ที่เชื่อมต่อกับ Service A ***
   เพื่อดึงข้อมูล user ผ่าน HTTP/REST API

   1. rest_client.py
      - REST API Client implementation
      - ส่ง HTTP GET request ไปยัง Service A (port 8000)
      - เรียก GET /user/1 จาก Service A

   วิธีการรัน:
      python service_C\rest_client.py
   ผลลัพธ์:
   ✅ Success: {'id': 1, 'name': 'Alice'}
      
 Mock Database

Service A ใช้ Mock Database (USERS_DB) สำหรับเก็บข้อมูล user:

| User ID | User Name |
|---------|-----------|
| 1       | Alice     |
| 2       | Bob       |
| 3       | Charlie   |
| 4       | David     |
| 5       | Eve       |
| 10      | Admin     |
| 99      | Guest     |
| 100     | Anonymous |


Dependencies (requirements.txt)

grpcio==1.60.0              
grpcio-tools==1.60.0        
protobuf==4.25.1            
requests==2.31.0            
fastapi==0.109.0            
uvicorn[standard]==0.27.0   
pydantic==2.5.3           
requests==2.31.0
