from fastapi import FastAPI

from s3_storage_app.config import config
from s3_storage_app.database import minio_client
from s3_storage_app.app import router

if not minio_client.bucket_exists(config.MINIO_BUCKET_NAME):
    minio_client.make_bucket(config.MINIO_BUCKET_NAME)

app = FastAPI(title=config.MEDIA_API_TITLE, debug=config.DEBUG)

app.include_router(router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)
