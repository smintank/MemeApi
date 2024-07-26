from pydantic import BaseModel


class SMeme(BaseModel):
    id: int
    text: str
    image_url: str
