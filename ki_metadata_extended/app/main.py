from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from app.pipeline.process_image import process_image
from app.utils.logger import log_upload
import traceback

app = FastAPI(
    title="KI Metadata Extended API",
    description="AI-powered image analysis with metadata extraction",
    version="1.0.0"
)

@app.get("/")
async def root():
    return {"message": "KI Metadata Extended API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    try:
        # Validate file type
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Validate file size (max 10MB)
        contents = await file.read()
        if len(contents) > 10 * 1024 * 1024:  # 10MB
            raise HTTPException(status_code=400, detail="File size too large (max 10MB)")
        
        log_upload(file.filename)
        result = process_image(contents)
        
        return JSONResponse(
            status_code=200,
            content={
                "filename": file.filename,
                "size": len(contents),
                "analysis": result
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error processing image: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/logs/uploads")
async def get_upload_logs():
    try:
        with open("/logs/uploads.log", "r") as f:
            logs = f.readlines()
        return {"uploads": logs[-100:]}  # Return last 100 entries
    except FileNotFoundError:
        return {"uploads": []}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading logs: {str(e)}")

@app.get("/logs/analysis")
async def get_analysis_logs():
    try:
        with open("/logs/analysis.log", "r") as f:
            logs = f.readlines()
        return {"analysis": logs[-100:]}  # Return last 100 entries
    except FileNotFoundError:
        return {"analysis": []}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading logs: {str(e)}")
