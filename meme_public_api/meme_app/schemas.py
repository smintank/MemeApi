from pydantic import BaseModel


class SMeme(BaseModel):
    id: int
    text: str
    image: str


class SCreateMeme(BaseModel):
    id: int
    text: str
    image_id: str
