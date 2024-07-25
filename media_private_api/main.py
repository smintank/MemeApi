from fastapi import FastAPI, UploadFile, File

app = FastAPI(title="S3_private_service")


@app.get("/download")
async def get_file():
    pass


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    pass