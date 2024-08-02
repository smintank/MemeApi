import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


class Config:
    MINIO_URL = os.getenv("MINIO_HOST") + ":" + os.getenv("MINIO_PORT", "9000")
    MINIO_ROOT_USER = os.getenv("MINIO_ROOT_USER", "minio_admin")
    MINIO_ROOT_PASSWORD = os.getenv("MINIO_ROOT_PASSWORD", "minio_admin")
    MINIO_BUCKET_NAME = os.getenv("MINIO_BUCKET_NAME", "media")
    MEDIA_API_TITLE = os.getenv("MEDIA_API_TITLE", "Media API")
    MEDIA_API_ENDPOINT = os.getenv("MEDIA_API_ENDPOINT", "images")
    DEBUG = bool(os.getenv("DEBUG", False))


config = Config()
