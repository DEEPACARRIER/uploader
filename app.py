from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import shutil
import os

app = FastAPI()

os.makedirs("static/uploads", exist_ok=True)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "upload.html",
        {"request": request}
    )


@app.post("/upload")
async def upload_video(
    video: UploadFile = File(...),
    caption: str = Form(...),
    upload_time: str = Form(...)
):
    file_path = f"static/uploads/{video.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(video.file, buffer)

    return {
        "message": "Video uploaded successfully",
        "video": video.filename,
        "caption": caption,
        "time": upload_time
    }
    import sqlite3

conn = sqlite3.connect("videos.db")
cursor = conn.cursor()

cursor.execute("""
INSERT INTO scheduled_videos(filename, caption, upload_time)
VALUES (?, ?, ?)
""", (video.filename, caption, upload_time))

conn.commit()
conn.close()