from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session

from .models import Meme
from .config import config
from .utils import get_api_data


def get_one_meme(db: Session, meme_id: int):
    meme = db.query(Meme).filter(Meme.id == meme_id).first()
    if not meme:
        raise HTTPException(status_code=404, detail="Meme Not Found")
    return meme


def get_all_memes(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Meme).offset(skip).limit(limit).all()


def create_meme(db: Session, text: str, image: UploadFile):
    api_data = get_api_data(config.MEDIA_API_URL, image)
    image_url = api_data['file_url']
    db_meme = Meme(text=text, image_url=image_url)
    db.add(db_meme)
    db.commit()
    db.refresh(db_meme)
    return db_meme


def update_meme(db: Session, meme_id: int, text: str, image: UploadFile):
    updated_meme = db.query(Meme).filter(Meme.id == meme_id).first()
    if updated_meme is None:
        raise HTTPException(status_code=404, detail="Meme not found")
    api_data = get_api_data(config.MEDIA_API_URL, image)
    image_url = api_data['file_url']

    updated_meme.image_url = image_url
    updated_meme.text = text
    db.commit()
    db.refresh(updated_meme)
    return updated_meme


def delete_meme(db: Session, meme_id: int):
    deleted_meme = db.query(Meme).filter(Meme.id == meme_id).first()
    if deleted_meme is None:
        raise HTTPException(status_code=404, detail="Meme not found")
    db.delete(deleted_meme)
    db.commit()
