from fastapi import FastAPI, HTTPException
from grpc_client import get_user_info

app = FastAPI()

# Route สำหรับดึงข้อมูลแมว (Service B ทำหน้าที่เป็น Gateway ไปหา gRPC)
@app.get("/cat/{cat_id}")
def read_cat(cat_id: int):
    # เรียกฟังก์ชัน get_user_info เพื่อไปดึงข้อมูลจาก Service A ผ่าน gRPC
    user_info = get_user_info(cat_id)

    # ถ้ามี error (เช่น หาไม่เจอ) ให้ส่ง 404
    if "error" in user_info:
        raise HTTPException(status_code=404, detail=user_info["error"])
    
    # ส่งข้อมูลกลับไปให้ User
    return user_info

if __name__ == "__main__":
    import uvicorn
    # รัน FastAPI ที่พอร์ต 8001
    uvicorn.run(app, host="0.0.0.0", port=8001)