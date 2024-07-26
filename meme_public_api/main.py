from fastapi import FastAPI, Depends, UploadFile, File
from sqlalchemy.orm import Session

from meme_app import crud, models, schemas
from meme_app.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Meme API")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/memes", response_model=list[schemas.SMeme])
async def get_all_memes(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_all_memes(db, skip=skip, limit=limit)


@app.get("/memes/{id}", response_model=schemas.SMeme)
async def get_meme(id: int, db: Session = Depends(get_db)):
    return crud.get_one_meme(db, id)


@app.post("/memes", response_model=schemas.SMeme)
async def create_memes(text: str, image: UploadFile = File(...), db: Session = Depends(get_db)):
    return crud.create_meme(db, text, image)


@app.put("/memes/{id}", response_model=schemas.SMeme)
async def update_meme(id: int, text: str, image: UploadFile = File(...), db: Session = Depends(get_db)):
    return crud.update_meme(db, id, text, image)


@app.delete("/memes/{id}", response_model=dict[str, str])
async def delete_meme(id: int, db: Session = Depends(get_db)):
    crud.delete_meme(db, id)
    return {"message": f"Meme with id: {id} has been deleted successfully"}
