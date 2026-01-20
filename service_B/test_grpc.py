import grpc
import user_pb2
import user_pb2_grpc

def test_get_user(user_id):
    """ทดสอบ GetUser ด้วย user_id ที่กำหนด"""
    # เชื่อมต่อกับ gRPC server
    channel = grpc.insecure_channel("localhost:50051")
    stub = user_pb2_grpc.UserServiceStub(channel)
    
    try:
        # เรียก GetUser
        response = stub.GetUser(user_pb2.UserRequest(id=user_id))
        print(f"✅ User ID {user_id}: {response.name}")
        return response
    except grpc.RpcError as e:
        print(f"❌ User ID {user_id}: {e.details()}")
        return None

def test_all_users():
    """ทดสอบ user ทั้งหมด"""
    print("=" * 50)
    print("🧪 Testing gRPC GetUser")
    print("=" * 50)
    
    # ทดสอบ user ที่มีอยู่
    test_ids = [1, 2, 3, 4, 5, 10, 99, 100]
    
    print("\n📋 Testing existing users:")
    for user_id in test_ids:
        test_get_user(user_id)
    
    # ทดสอบ user ที่ไม่มี
    print("\n📋 Testing non-existent users:")
    test_get_user(999)
    test_get_user(0)
    test_get_user(-1)
    
    print("\n" + "=" * 50)
    print("✅ Test completed!")
    print("=" * 50)

if __name__ == "__main__":
    test_all_users()
