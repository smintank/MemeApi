from typing import Sequence

from fastapi import HTTPException
from sqlalchemy import Row
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError


async def get_item(db: AsyncSession, model, item_id: int) -> Row:
    item = (await db.scalars(select(model).where(model.id == item_id))).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item Not Found")
    return item


async def get_items(db: AsyncSession, model, skip: int = 0, limit: int = 10) -> Sequence[Row]:
    try:
        return (await db.scalars(select(model).offset(skip).limit(limit))).all()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))


async def create_item(db: AsyncSession, model, **kwargs) -> Row:
    try:
        db_meme = model(**kwargs)
        db.add(db_meme)
        await db.commit()
        await db.refresh(db_meme)
        return db_meme
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


async def update_item(db: AsyncSession, model, item_id: int, **kwargs) -> Row:
    try:
        item = await get_item(db, model, item_id)
        [setattr(item, key, value) for key, value in kwargs.items()]
        await db.commit()
        await db.refresh(item)
        return item
    except HTTPException:
        raise HTTPException(status_code=404, detail="Item not found")
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


async def delete_item(db: AsyncSession, model, item_id: int) -> None:
    try:
        item = await get_item(db, model, item_id)
        await db.delete(item)
        await db.commit()
    except HTTPException:
        raise HTTPException(status_code=404, detail="Item not found")
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
