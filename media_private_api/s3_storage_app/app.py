from io import BytesIO

from fastapi import UploadFile, File, HTTPException, APIRouter
from fastapi.responses import StreamingResponse, JSONResponse
from minio import S3Error

from .config import config
from .database import minio_client


router = APIRouter(prefix='/' + config.MEDIA_API_ENDPOINT)


@router.post("/")
async def upload_file(file: UploadFile = File(...)) -> JSONResponse:
    try:
        created_file = minio_client.put_object(
            bucket_name=config.MINIO_BUCKET_NAME,
            object_name=file.filename,
            data=file.file,
            length=-1,
            part_size=10 * 1024 * 1024,
            content_type=file.content_type
        )
        return JSONResponse(
            content={
                'object_name': created_file.object_name,
                'bucket_name': created_file.bucket_name,
            },
            status_code=201
        )
    except S3Error:
        raise HTTPException(status_code=404, detail="File not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{file_id}")
async def get_file(file_id: str):
    print(file_id)
    try:
        response = minio_client.get_object(config.MINIO_BUCKET_NAME, object_name=file_id)
        file_content = response.read()
        file_stream = BytesIO(file_content)
        return StreamingResponse(
            file_stream, media_type='application/octet-stream',
            headers={"Content-Disposition": f"attachment; filename={file_id}"}
        )
    except S3Error:
        raise HTTPException(status_code=404, detail="File not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{file_id}")
async def delete_file(file_id: str):
    try:
        minio_client.remove_object(config.MINIO_BUCKET_NAME, object_name=file_id)
        return JSONResponse(content={"message": "File deleted successfully"}, status_code=200)
    except S3Error:
        raise HTTPException(status_code=404, detail="File not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
