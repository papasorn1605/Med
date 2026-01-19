import grpc
import user_pb2
import user_pb2_grpc

import os

def get_user_info(user_id):
    # เชื่อมต่อกับ Service A
    # อ่านค่า Host จาก Environment Variable (ถ้าไม่มีให้ใช้ localhost)
    host = os.getenv("GRPC_SERVER_HOST", "localhost")
    
    # สร้าง Channel สำหรับเชื่อมต่อ gRPC ไปที่พอร์ต 50051
    with grpc.insecure_channel(f'{host}:50051') as channel:
        stub = user_pb2_grpc.UserServiceStub(channel)
        
        try:
            # เรียกใช้ฟังก์ชัน GetUser ของ Service A
            response = stub.GetUser(user_pb2.UserRequest(user_id=user_id))
            # แปลงข้อมูลจาก Object เป็น Dictionary เพื่อส่งกลับไป
            return {
                "id": response.id,
                "name": response.name,
                "origin": response.origin,
                "temperament": response.temperament
            }
        except grpc.RpcError as e:
            # จัดการ Error ถ้าเกิดปัญหา (เช่น หาไม่เจอ)
            return {"error": e.details()}