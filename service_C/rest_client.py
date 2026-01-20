
import requests
import os

def get_user():
    """
    ฟังก์ชันสำหรับเรียก GET /user/1 จาก Service A ผ่าน REST API
    
    Configuration:
        - ใช้ environment variable REST_API_URL
        - Default: http://localhost:8000 (สำหรับรันแบบ local)
        - Docker: http://service_a:8000 (ตั้งค่าใน docker-compose.yml)
    
    Request ที่ส่งไป Service A:
        HTTP Method: GET
        URL: {base_url}/user/1
        Headers: (default)
    
    Response ที่ได้รับจาก Service A:
        HTTP Status: 200 OK
        Content-Type: application/json
        Body: {
            "id": 1,
            "name": "Alice"
        }
    
    Error Handling:
        - ConnectionError: Service A ไม่ทำงาน
        - 404 Not Found: ไม่มี user ID นี้
        - 500 Internal Server Error: Server error
    """
    
    # อ่าน REST API URL จาก environment variable
    # ถ้าไม่มีให้ใช้ http://localhost:8000 (สำหรับรันแบบ local)
    base_url = os.getenv("REST_API_URL", "http://localhost:8000")
    
    try:
        # ===== STEP 1: ส่ง HTTP GET Request =====
        # เรียก GET /user/1 เพื่อดึงข้อมูล user ID 1
        r = requests.get(f"{base_url}/user/1")
        
        # ===== STEP 2: ตรวจสอบ HTTP Status =====
        # ถ้า status code ไม่ใช่ 2xx จะ raise HTTPError
        r.raise_for_status()
        
        # ===== STEP 3: Parse JSON Response =====
        # แปลง response body จาก JSON string เป็น Python dict
        user_data = r.json()
        
        # ===== STEP 4: แสดงผลลัพธ์ =====
        print(f"✅ Success: {user_data}")
        return user_data
        
    except requests.exceptions.ConnectionError:
        # กรณีเชื่อมต่อไม่ได้ (Service A ไม่ทำงาน)
        print(f"❌ Connection Error: Cannot connect to {base_url}")
        print("Make sure Service A is running!")
        
    except requests.exceptions.RequestException as e:
        # กรณี error อื่นๆ (404, 500, timeout, etc.)
        print(f"❌ Error: {e}")
