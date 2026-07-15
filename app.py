from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import shutil
import os

app = FastAPI()

# Folders create karo agar na hon
os.makedirs("static/uploads", exist_ok=True)
os.makedirs("templates", exist_ok=True)

# Static files mount
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates setup
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="upload.html"
    )


@app.post("/upload")
async def upload_video(
    video: UploadFile = File(...),
    caption: str = Form(...),
    upload_time: str = Form(...)
):
    try:
        file_path = f"static/uploads/{video.filename}"

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(video.file, buffer)

        return JSONResponse({
            "success": True,
            "message": "Video uploaded successfully",
            "video_name": video.filename,
            "caption": caption,
            "scheduled_time": upload_time
        })

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": str(e)
            }
        )


@app.get("/health")
async def health():
    return {"status": "running"}
