import uuid

from fastapi import UploadFile, File, APIRouter
from fastapi.responses import JSONResponse

from .crud import get_items, get_item, create_item, update_item, delete_item
from .database import DBSessionDep
from .schemas import SMeme
from .models import Meme
from .config import config
from .utils import get_image_data, store_image


router = APIRouter(prefix='/' + config.MEME_API_ENDPOINT)


@router.get("/{meme_id}", response_model=SMeme)
async def get_meme(db: DBSessionDep, meme_id: int):
    meme_obj = await get_item(db, model=Meme, item_id=meme_id)
    meme_obj.image = await get_image_data(image_id=meme_obj.image_id)
    return meme_obj


@router.get("/", response_model=list[SMeme])
async def get_memes(db: DBSessionDep, skip: int = 0, limit: int = 10):
    memes = await get_items(db, Meme, skip=skip, limit=limit)
    return [SMeme(id=meme.id, text=meme.text, image=await get_image_data(meme.image_id)) for meme in memes]


@router.post("/", response_model=SMeme)
async def create_meme(db: DBSessionDep, text: str, image: UploadFile = File(...)):
    image_id = await store_image(image)
    meme_obj = await create_item(db, Meme, text=text, image_id=image_id)
    return SMeme(id=meme_obj.id, text=meme_obj.text, image=image_id)


@router.put("/{meme_id}", response_model=SMeme)
async def update_meme(db: DBSessionDep, meme_id: int, text: str, image: UploadFile = File(...)):
    image_data = await store_image(image, str(uuid.uuid4()))
    return await update_item(db, Meme, meme_id, text=text, image=image_data)


@router.delete("/{meme_id}", response_model=dict[str, str])
async def delete_meme(db: DBSessionDep, meme_id: int):
    await delete_item(db, Meme, meme_id)
    return JSONResponse(
        content={"message": f"Meme with id: {meme_id} has been deleted successfully"},
        status_code=200
    )
