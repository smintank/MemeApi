from minio import Minio

from .config import config

minio_client = Minio(
    endpoint=config.MINIO_URL,
    access_key=config.MINIO_ROOT_USER,
    secret_key=config.MINIO_ROOT_PASSWORD,
    secure=False
)
