# Dockerfile for FastAPI
FROM python:3.10.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "src:app", "--host", "0.0.0.0", "--port", "8000"]
