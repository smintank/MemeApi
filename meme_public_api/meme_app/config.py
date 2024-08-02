import os

from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())


class Config:
    MEME_API_TITLE = os.getenv('MEME_API_TITLE', 'Meme API')
    MEME_API_ENDPOINT = os.getenv('MEME_API_ENDPOINT', 'memes')
    MEDIA_API_URL = f"http://{os.getenv('MEDIA_API_HOST', 'media_api')}:{os.getenv('MEDIA_API_PORT', '8001')}"
    MEDIA_API_ENDPOINT = os.getenv('MEDIA_API_ENDPOINT', 'images')

    POSTGRES_DB = os.getenv('POSTGRES_DB', 'meme_db')
    POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'postgres')
    POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5432')
    POSTGRES_USER = os.getenv('POSTGRES_USER', 'meme_user')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'meme_password')

    DEBUG = bool(os.getenv('DEBUG', False))


config = Config()
