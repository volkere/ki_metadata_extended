from fastapi import FastAPI, UploadFile, File
from app.pipeline.process_image import process_image
from app.utils.logger import log_upload

app = FastAPI()

@app.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    contents = await file.read()
    log_upload(file.filename)
    result = process_image(contents)
    return result
