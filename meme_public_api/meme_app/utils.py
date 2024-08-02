import base64
import uuid

import httpx
from fastapi import HTTPException, UploadFile

from .config import config

ENDPOINT = config.MEDIA_API_URL + '/' + config.MEDIA_API_ENDPOINT


async def store_image(file: UploadFile, filename: str = None) -> str:
    filename = filename if filename else str(uuid.uuid4())

    async with httpx.AsyncClient(follow_redirects=True) as client:
        files = {'file': (filename, await file.read(), file.content_type)}
        try:
            print(ENDPOINT)
            response = await client.post(url=ENDPOINT, files=files)
            response.raise_for_status()
            json_response = response.json()
            return json_response['object_name']
        except KeyError:
            raise HTTPException(status_code=500, detail="Error to store image")
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=str(e))
        except httpx.RequestError as e:
            raise HTTPException(status_code=500, detail=str(e))


async def get_image_data(image_id: str) -> str:
    try:
        async with httpx.AsyncClient(follow_redirects=True) as client:
            response = await client.get(url=ENDPOINT + '/' + image_id)
            response.raise_for_status()
            file = await response.aread()
        return base64.b64encode(file).decode("utf-8")
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=str(exc))
    except httpx.RequestError as exc:
        raise HTTPException(status_code=500, detail=str(exc))


async def delete_image_data(image_id: str) -> dict[str, str]:
    try:
        async with httpx.AsyncClient(follow_redirects=True) as client:
            response = await client.delete(url=ENDPOINT + '/' + image_id)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=str(exc))
    except httpx.RequestError as exc:
        raise HTTPException(status_code=500, detail=str(exc))
