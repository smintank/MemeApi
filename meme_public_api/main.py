from fastapi import FastAPI, UploadFile, File

app = FastAPI()


@app.get("/memes")
async def get_all_memes():
    return {"All memes"}


@app.get("/memes/{id}")
async def get_meme(id: int):
    return {f"{id} meme"}


@app.post("/memes")
async def add_memes(text: str, image: UploadFile = File(...)):
    return {"New meme has been added!"}


@app.put("/memes/{id}")
async def update_meme(id: int, text: str, image: UploadFile = File(...)):
    return {f"Meme {id} has been updated!"}


@app.delete("/memes/{id}")
async def delete_meme(id: int):
    return {f"Meme {id} has been deleted!"}
