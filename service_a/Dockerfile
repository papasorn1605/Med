FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY service_a/ .
COPY service_a/cat_breeds.json .

CMD ["python", "main.py"]
