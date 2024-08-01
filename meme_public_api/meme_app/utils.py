import base64

import httpx
from fastapi import HTTPException, UploadFile


async def get_image_data(image_id):
    url = f'http://media_private_api:8001/storage/{image_id}'
    print(url)
    try:
        async with httpx.AsyncClient(follow_redirects=True) as client:
            response = await client.get(url)
            response.raise_for_status()
            file = response.read()
            base64_encoded_data = base64.b64encode(file)
        return base64_encoded_data
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=str(exc))
    except httpx.RequestError as exc:
        raise HTTPException(status_code=500, detail=str(exc))


async def store_image_data(file: UploadFile, filename: str):
    url = 'http://media_private_api:8001/storage/'
    async with httpx.AsyncClient(follow_redirects=True) as client:
        files = {'file': (filename, await file.read(), file.content_type)}
        try:
            response = await client.post(url, files=files)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=str(e))
        except httpx.RequestError as e:
            raise HTTPException(status_code=500, detail=str(e))


async def delete_image_data(image_id):
    url = f'http://media_private_api:8001/storage/{image_id}'
    try:
        async with httpx.AsyncClient(follow_redirects=True) as client:
            response = await client.delete(url)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=str(exc))
    except httpx.RequestError as exc:
        raise HTTPException(status_code=500, detail=str(exc))
