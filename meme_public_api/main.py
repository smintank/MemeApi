from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import FastAPI, Depends, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession

from meme_app import crud
from meme_app.database import AsyncSessionLocal
from meme_app.schemas import SMeme, SCreateMeme
from meme_app.models import Meme
from meme_app.config import config


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session


DBSessionDep = Annotated[AsyncSession, Depends(get_db)]


app = FastAPI(title=config.MEME_API_TITLE, lifespan=lifespan)


@app.get("/memes/{meme_id}", response_model=SMeme)
async def get_meme(db: DBSessionDep, meme_id: int):
    return await crud.get_item(db, Meme, meme_id)


@app.get("/memes", response_model=list[SMeme])
async def get_memes(db: DBSessionDep, skip: int = 0, limit: int = 10):
    return await crud.get_items(db, Meme, skip=skip, limit=limit)


@app.post("/memes", response_model=SCreateMeme)
async def create_meme(db: DBSessionDep, text: str, image: UploadFile = File(...)):
    return await crud.create_item(db, Meme, text, image)


@app.put("/memes/{meme_id}", response_model=SCreateMeme)
async def update_meme(db: DBSessionDep, meme_id: int, text: str, image: UploadFile = File(...)):
    return await crud.update_item(db, Meme, meme_id, text, image)


@app.delete("/memes/{meme_id}", response_model=dict[str, str])
async def delete_meme(db: DBSessionDep, meme_id: int, delete_image: bool = True):
    await crud.delete_item(db, Meme, meme_id, delete_image)
    return {"message": f"Meme with id: {meme_id} has been deleted successfully"}
