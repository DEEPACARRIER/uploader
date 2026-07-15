import requests
from instagram.config import (
    INSTAGRAM_ACCESS_TOKEN,
    INSTAGRAM_ACCOUNT_ID
)

def upload_reel(video_url, caption):
    create_url = (
        f"https://graph.facebook.com/v23.0/"
        f"{INSTAGRAM_ACCOUNT_ID}/media"
    )

    payload = {
        "media_type": "REELS",
        "video_url": video_url,
        "caption": caption,
        "access_token": INSTAGRAM_ACCESS_TOKEN
    }

    response = requests.post(create_url, data=payload)

    print(response.json())
