from fastapi import FastAPI
from meme_app.database import lifespan
from meme_app.config import config
from meme_app.app import router

app = FastAPI(
    title=config.MEME_API_TITLE,
    lifespan=lifespan,
    debug=config.DEBUG
)

app.include_router(router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
