import httpx
from fastapi import HTTPException, UploadFile


# async def get_api_data(api_url: str, image):
#     try:
#         async with httpx.AsyncClient() as client:
#             response = await client.get(api_url)
#             response.raise_for_status()
#             data = response.json()
#             return data
#     except httpx.HTTPStatusError as exc:
#         raise HTTPException(status_code=exc.response.status_code,
#                             detail=str(exc))
#     except httpx.RequestError as exc:
#         raise HTTPException(status_code=500, detail=str(exc))

def get_api_data(api_url: str, image: UploadFile) -> dict:
    return {'file_url': 'localhost:8000/test.jpg'}
