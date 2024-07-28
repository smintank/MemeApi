import os

from fastapi import FastAPI, UploadFile, File
from minio import S3Error, Minio

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

MINIO_URL = os.getenv("MINIO_URL")
MINIO_ROOT_USER = os.getenv("MINIO_ROOT_USER")
MINIO_ROOT_PASSWORD = os.getenv("MINIO_ROOT_PASSWORD")
MINIO_BUCKET_NAME = os.getenv("MINIO_BUCKET_NAME")


minio_client = Minio(
    endpoint=MINIO_URL,
    access_key=MINIO_ROOT_USER,
    secret_key=MINIO_ROOT_PASSWORD,
    secure=False
)

if not minio_client.bucket_exists(MINIO_BUCKET_NAME):
    minio_client.make_bucket(MINIO_BUCKET_NAME)

app = FastAPI(title="Private Media API")


@app.get("/download/{file_id}")
async def get_file(file_id: str):
    try:
        response = minio_client.get_object(MINIO_BUCKET_NAME, file_id)
        return {"id": file_id, "content": response.data.decode('utf-8')}
    except S3Error as e:
        return {"error": str(e)}


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    return await file.read()
