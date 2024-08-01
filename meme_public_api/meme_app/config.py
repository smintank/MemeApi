import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


class Config:
    MEME_API_TITLE = os.getenv('MEME_API_TITLE')
    DATABASE_URL = os.getenv('DATABASE_URL')
    MEDIA_API_URL = os.getenv('MEDIA_API_URL')

    POSTGRES_DB = os.getenv('POSTGRES_DB')
    POSTGRES_HOST = os.getenv('POSTGRES_HOST')
    POSTGRES_PORT = os.getenv('POSTGRES_PORT')
    POSTGRES_USER = os.getenv('POSTGRES_USER')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')

    DEBUG = bool(os.getenv('DEBUG', False))


config = Config()
