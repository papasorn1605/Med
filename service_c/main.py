from fastapi import FastAPI, HTTPException
import requests
import os
import uvicorn

app = FastAPI()

# อ่านค่า Host ของ Service A จาก Environment Variable (ถ้าไม่มีให้ใช้ localhost)
SERVICE_A_HOST = os.getenv("SERVICE_A_HOST", "localhost")
# สร้าง URL สำหรับเรียก Service A (พอร์ต 8000)
SERVICE_A_URL = f"http://{SERVICE_A_HOST}:8000"

# Route สำหรับดึงข้อมูลแมว (Service C ทำหน้าที่เป็น Gateway ไปหา REST API)
@app.get("/cat/{cat_id}")
def get_cat(cat_id: int):
    try:
        # เรียก Service A ผ่าน REST API (ใช้ requests)
        response = requests.get(f"{SERVICE_A_URL}/cat/{cat_id}")
        
        # ถ้าได้สถานะ 200 (OK) ให้ส่งข้อมูลกลับ
        if response.status_code == 200:
            return response.json()
        # ถ้าได้ 404 (ไม่เจอ) ให้ส่ง 404 กลับ
        elif response.status_code == 404:
            raise HTTPException(status_code=404, detail="Cat not found in Service A")
        # กรณีอื่นๆ ให้ส่ง 500
        else:
            raise HTTPException(status_code=500, detail="Service A returned an error")
    except requests.exceptions.ConnectionError:
        # ถ้าเชื่อมต่อไม่ได้ ให้ส่ง 503
        raise HTTPException(status_code=503, detail="Could not connect to Service A")

if __name__ == "__main__":
    # รัน FastAPI ที่พอร์ต 8002
    uvicorn.run(app, host="0.0.0.0", port=8002)
