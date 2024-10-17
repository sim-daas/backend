'''
from fastapi import FastAPI
from fastapi.responses import FileResponse
import os

app = FastAPI()

# Define the path to your GIF file
GIF_PATH = os.path.join(os.getcwd(), "image.jpg")

@app.get("/image")
async def get_image():
    """
    Serve the GIF as a response.
    """
    if os.path.exists(GIF_PATH):
        return FileResponse(GIF_PATH, media_type="image/jpg")
    else:
        return {"error": "GIF not found"}
'''

from fastapi import FastAPI, Form
from pymongo import MongoClient
from pydantic import BaseModel, EmailStr
import os

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Can be adjusted to the exact origin if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB client setup (replace with your MongoDB URI)
MONGO_URI = os.getenv('MONGO_URI')
client = MongoClient(MONGO_URI)
db = client["your_database"]
collection = db["submissions"]

# Pydantic model for form data validation


class Submission(BaseModel):
    name: str
    email: EmailStr
    subject: str = None
    reason: str


@app.post("/submit")
def submit_form(
    name: str = Form(...),
    email: str = Form(...),
    subject: str = Form(None),
    reason: str = Form(...)
):
    # Create a dictionary to save in MongoDB
    submission_data = {
        "name": name,
        "email": email,
        "subject": subject,
        "reason": reason
    }

    # Insert into MongoDB
    result = collection.insert_one(submission_data)
    return {"message": "Submission successful", "id": str(result.inserted_id)}
