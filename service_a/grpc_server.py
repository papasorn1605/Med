# service_a/grpc_server.py

import grpc
from concurrent import futures
import time
import json
import os

# นำเข้าคลาสที่ถูก generate มาจากไฟล์ .proto
import user_pb2_grpc
import user_pb2

# ฟังก์ชันโหลดข้อมูลจากไฟล์ JSON (cat_breeds.json)
def load_data():
    with open('cat_breeds.json', 'r') as f:
        data = json.load(f)
        # แปลงข้อมูลเป็น Dictionary โดยใช้ ID เป็น key เพื่อให้ค้นหาง่าย
        return {item['id']: item for item in data}

# โหลดข้อมูลเก็บไว้ในตัวแปร USER_DB
USER_DB = load_data()

# สร้างคลาสสำหรับจัดการคำขอ gRPC (สืบทอดมาจากคลาสที่ generate ไว้)
class UserServiceServicer(user_pb2_grpc.UserServiceServicer):

    # ฟังก์ชัน GetUser ที่ถูกเรียกเมื่อ Client ขอข้อมูล
    def GetUser(self, request, context):
        user_id = request.user_id
        # ค้นหาข้อมูลจาก DB
        user = USER_DB.get(user_id)

        if user:
            # ถ้าเจอข้อมูล ให้ส่งกลับไปในรูปแบบ UserReply (ตามที่นิยามใน proto)
            return user_pb2.UserReply(
                id=user["id"],
                name=user["name"],
                origin=user["origin"],
                temperament=user["temperament"]
            )
        else:
            # ถ้าไม่เจอ ให้ส่ง Error NOT_FOUND กลับไป
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"Cat breed with ID {user_id} not found.")
            return user_pb2.UserReply()

# ฟังก์ชันสำหรับเริ่มรัน Server
def serve():
    # สร้าง Server โดยรองรับได้สูงสุด 10 threads พร้อมกัน
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    # ลงทะเบียน Servicer เข้ากับ Server
    user_pb2_grpc.add_UserServiceServicer_to_server(UserServiceServicer(), server)

    # เปิดพอร์ต 50051 สำหรับรับการเชื่อมต่อ
    server.add_insecure_port('[::]:50051')
    print("Starting gRPC server on port 50051...")
    server.start()
    # รอจนกว่าจะมีการสั่งปิด
    server.wait_for_termination()