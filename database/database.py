import sqlite3

conn = sqlite3.connect("videos.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS scheduled_videos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT,
    caption TEXT,
    upload_time TEXT,
    status TEXT DEFAULT 'pending'
)
""")

conn.commit()
conn.close()
