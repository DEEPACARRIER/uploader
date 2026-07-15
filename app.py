from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import shutil
import os
import sqlite3

app = FastAPI()

# Create uploads folder if it doesn't exist
os.makedirs("static/uploads", exist_ok=True)

# Mount static folder
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")


# -------------------------------
# Home Page
# -------------------------------
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "upload.html",
        {"request": request}
    )


# -------------------------------
# Upload Video
# -------------------------------
@app.post("/upload")
async def upload_video(
    video: UploadFile = File(...),
    caption: str = Form(...),
    upload_time: str = Form(...)
):

    # Save uploaded file
    file_path = f"static/uploads/{video.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(video.file, buffer)

    # Save to SQLite database
    conn = sqlite3.connect("videos.db")
    cursor = conn.cursor()

    # Create table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scheduled_videos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            caption TEXT,
            upload_time TEXT
        )
    """)

    cursor.execute("""
        INSERT INTO scheduled_videos
        (filename, caption, upload_time)
        VALUES (?, ?, ?)
    """, (
        video.filename,
        caption,
        upload_time
    ))

    conn.commit()
    conn.close()

    return {
        "success": True,
        "message": "Video uploaded successfully",
        "video": video.filename,
        "caption": caption,
        "upload_time": upload_time
    }
