import os
from io import BytesIO

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
from minio import S3Error, Minio

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

MINIO_URL = os.getenv("MINIO_HOST") + ":" + os.getenv("MINIO_PORT")
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


@app.post("/storage/")
async def upload_file(file: UploadFile = File(...)):
    try:
        created_file = minio_client.put_object(
            bucket_name=MINIO_BUCKET_NAME,
            object_name=file.filename,
            data=file.file,
            length=-1,
            part_size=10 * 1024 * 1024,
            content_type=file.content_type
        )
        return created_file
    except S3Error:
        raise HTTPException(status_code=404, detail="File not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/storage/{file_id}")
async def get_file(file_id: str):
    print(file_id)
    try:
        response = minio_client.get_object(MINIO_BUCKET_NAME, file_id)
        file_content = response.read()
        file_stream = BytesIO(file_content)
        return StreamingResponse(
            file_stream, media_type='application/octet-stream',
            headers={"Content-Disposition": f"attachment; filename={file_id}"}
        )
    except S3Error:
        raise HTTPException(status_code=404, detail="File not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/storage/{file_id}")
async def delete_file(file_id: str):
    try:
        minio_client.remove_object(MINIO_BUCKET_NAME, object_name=file_id)
        return JSONResponse(content={"message": "File deleted successfully"}, status_code=200)
    except S3Error:
        raise HTTPException(status_code=404, detail="File not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
