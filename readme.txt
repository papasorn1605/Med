Project Name: milk347

Project Tree:
|-- requirements.txt
|-- docker-compose.yml
|-- service_a
|   |-- Dockerfile
|   |-- cat_breeds.json
|   |-- grpc_server.py
|   |-- main.py
|   |-- proto
|       |-- user.proto
|-- service_b
|   |-- Dockerfile
|   |-- grpc_client.py
|   |-- main.py
|   |-- proto
|       |-- user.proto
|-- service_c
|   |-- Dockerfile
|   |-- main.py
|   |-- proto
|       |-- user.proto

คำอธิบายการทำงาน (System Explanation):
1. Service A (Main Server):
   - ทำหน้าที่เป็น Database Server เก็บข้อมูลสายพันธุ์แมว (ในไฟล์ cat_breeds.json)
   - ให้บริการ 2 ช่องทาง:
     1. gRPC (Port 50051): สำหรับ Service B
     2. REST API (Port 8000): สำหรับ Service C

2. Service B (gRPC Client):
   - ทำหน้าที่เป็น API Gateway รับ Request จาก User
   - ดึงข้อมูลจาก Service A ผ่านโปรโตคอล gRPC
   - รันที่ Port 8001

3. Service C (REST Client):
   - ทำหน้าที่เป็น API Gateway รับ Request จาก User
   - ดึงข้อมูลจาก Service A ผ่าน REST API (HTTP Request)
   - รันที่ Port 8002

Request/Response Flow:
- User -> Service B (GET /cat/{id}) -> [gRPC] -> Service A (ค้นหา DB) -> [gRPC Reply] -> Service B -> User (JSON)
- User -> Service C (GET /cat/{id}) -> [HTTP GET] -> Service A (ค้นหา DB) -> [HTTP Response] -> Service C -> User (JSON)

วิธีการรัน (How to Run):
1. ตรวจสอบว่าเปิด Docker Desktop แล้ว
2. รันคำสั่ง: docker compose up --build
3. รอจนกว่าจะขึ้นว่า Started server process ครบทุก Service

ผลลัพธ์ที่ควรได้ (Expected Results):
- Service A (Health Check): http://localhost:8000/ -> {"message": "FastAPI is running alongside gRPC server!"}
- Service A (Data): http://localhost:8000/cat/1 -> ข้อมูลแมว Siamese
- Service B (via gRPC): http://localhost:8001/cat/1 -> ข้อมูลแมว Siamese (เหมือน A)
- Service C (via REST): http://localhost:8002/cat/1 -> ข้อมูลแมว Siamese (เหมือน A)
