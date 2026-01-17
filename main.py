from fastapi import FastAPI, Header
import yt_dlp as youtube_dl
import os

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
    
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'noplaylist': True,
            'outtmpl': '%(title)s.%(ext)s', 
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        return {"status": "ok", "url": url}
    except Exception as e:
        return {"error": str(e)}