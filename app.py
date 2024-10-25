from fastapi import FastAPI, Form
from pymongo import MongoClient
from pydantic import BaseModel, EmailStr
import os

app = FastAPI()

# MongoDB client setup (replace with your MongoDB URI)
MONGO_URI = os.getenv('MONGO_URI')
client = MongoClient(MONGO_URI)
db = client["your_database"]
collection = db["submissions"]
meal_collection = db["meal_feedback"]

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


class MealFeedback(BaseModel):
    meal: str
    rating: int
    message: str


@app.post("/submit_meal")
def submit_meal(
    meal: str = Form(...),
    rating: int = Form(...),
    message: str = Form(...)
):
    feedback_data = {
        "meal": meal,
        "rating": rating,
        "message": message
    }
    result = meal_collection.insert_one(feedback_data)
    return {"message": "Feedback submitted successfully", "id": str(result.inserted_id)}


@app.get("/average_ratings")
def get_average_ratings():
    pipeline = [
        {
            "$group": {
                "_id": "$meal",
                "average_rating": {"$avg": "$rating"}
            }
        }
    ]
    averages = list(meal_collection.aggregate(pipeline))
    return {"average_ratings": averages}
