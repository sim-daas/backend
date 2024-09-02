from fastapi import FastAPI
from fastapi.responses import FileResponse
import os

app = FastAPI()

# Define the path to your GIF file
GIF_PATH = os.path.join(os.getcwd(), "image.gif")

@app.get("/image")
async def get_image():
    """
    Serve the GIF as a response.
    """
    if os.path.exists(GIF_PATH):
        return FileResponse(GIF_PATH, media_type="image/gif")
    else:
        return {"error": "GIF not found"}
