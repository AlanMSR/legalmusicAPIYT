from fastapi import FastAPI, Header
from fastapi.responses import FileResponse
import yt_dlp as youtube_dl
import os
import uuid

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello!"}

@app.post("/download-youtube-music")
async def download_youtube_music(
    url: str,
    api_key: str = Header(None)
):
    if api_key != os.environ.get('API_KEY'):
        return {"error": "Invalid API Key"}
    
    file_id = str(uuid.uuid4())
    output_path = f"/tmp/{file_id}.%(ext)s"

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'noplaylist': True,
        'outtmpl': output_path,
        'quiet': True,
    }

    try:

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        final_path = f"/tmp/{file_id}.mp3"

        return FileResponse(
            path=final_path,
            media_type="audio/mpeg",
            filename="audio.mp3",
        )
        
    except Exception as e:
        return {"error": str(e)}
    
    finally:
        if os.path.exists(final_path):
            os.remove(final_path)