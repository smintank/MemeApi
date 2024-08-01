import uuid

from fastapi import HTTPException, UploadFile
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from .utils import store_image_data, get_image_data, delete_image_data
from .schemas import SMeme, SCreateMeme


async def get_item(db: AsyncSession, model, item_id: int):
    result = await db.execute(select(model).filter(model.id == item_id))
    meme = result.scalar()
    if not meme:
        raise HTTPException(status_code=404, detail="Meme Not Found")
    image = await get_image_data(meme.image_id)
    return SMeme(id=item_id, text=meme.text, image=image)


async def get_items(db: AsyncSession, model, skip: int = 0, limit: int = 10) -> list[SMeme]:
    result = await db.execute(select(model).offset(skip).limit(limit))
    memes = result.scalars().all()
    memes_list = []
    for meme in memes:
        image = await get_image_data(meme.image_id)
        memes_list.append(SMeme(id=meme.id, text=meme.text, image=image))
    return memes_list


async def create_item(db: AsyncSession, model, text: str, image: UploadFile):
    stored_image = await store_image_data(image, str(uuid.uuid4()))
    image_id = stored_image['_object_name']
    db_meme = model(text=text, image_id=image_id)
    db.add(db_meme)
    await db.commit()
    await db.refresh(db_meme)
    return db_meme


async def update_item(db: AsyncSession, model, item_id: int, text: str, image: UploadFile):
    result = await db.execute(select(model).filter(model.id == item_id))
    updated_meme = result.scalar()
    if updated_meme is None:
        raise HTTPException(status_code=404, detail="Meme not found")
    stored_image = await store_image_data(image, str(uuid.uuid4()))
    updated_meme.image_id = stored_image['_object_name']
    updated_meme.text = text
    await db.commit()
    await db.refresh(updated_meme)
    return SCreateMeme(id=item_id, text=updated_meme.text, image_id=updated_meme.image_id)


async def delete_item(db: AsyncSession, model, item_id: int, delete_image: bool = True):
    result = await db.execute(select(model).filter(model.id == item_id))
    deleted_meme = result.scalar()
    if deleted_meme is None:
        raise HTTPException(status_code=404, detail="Meme not found")
    if delete_image:
        await delete_image_data(deleted_meme.image_id)
    await db.delete(deleted_meme)
    await db.commit()
