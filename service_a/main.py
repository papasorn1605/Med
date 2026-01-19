import threading
import uvicorn
from fastapi import FastAPI

# นำเข้าฟังก์ชันสำหรับรัน gRPC server
from grpc_server import serve

# สร้างตัวแอป FastAPI
app = FastAPI()

# Route สำหรับตรวจสอบสถานะระบบ (Health Check)
@app.get("/")
def read_root():
    return {"message": "FastAPI is running alongside gRPC server!"}

# นำเข้าฐานข้อมูล (USER_DB) จากไฟล์ grpc_server
from grpc_server import USER_DB
from fastapi import HTTPException

# Route สำหรับดึงข้อมูลแมวผ่าน REST API
# ตัวอย่างการเรียก: http://localhost:8000/cat/1
@app.get("/cat/{cat_id}")
def get_cat(cat_id: int):
    # ค้นหาข้อมูลแมวจาก ID ในฐานข้อมูล
    user = USER_DB.get(cat_id)
    if user:
        return user
    # ถ้าไม่เจอให้ส่ง error 404
    raise HTTPException(status_code=404, detail="User not found")

# ฟังก์ชันสำหรับรัน gRPC server แยกใน Thread ต่างหาก
def start_grpc_server():
    serve()

if __name__ == "__main__":
    # เริ่มต้น gRPC server ใน Thread แยก (เพื่อให้ทำงานพร้อมกับ FastAPI ได้)
    grpc_thread = threading.Thread(target=start_grpc_server, daemon=True)
    grpc_thread.start()

    # เริ่มต้น FastAPI server ที่พอร์ต 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)