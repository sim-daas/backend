from fastapi import FastAPI, Form, Query, HTTPException
from pymongo import MongoClient
from pydantic import BaseModel, EmailStr
import os
from datetime import datetime
from typing import Optional

app = FastAPI()

# MongoDB client setup (replace with your MongoDB URI)
MONGO_URI = os.getenv('MONGO_URI')
client = MongoClient(MONGO_URI)
db = client["your_database"]
collection = db["submissions"]
meal_collection = db["meal_feedback"]
ADMIN_KEY = os.getenv('ADMIN_KEY')

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

   weekday = datetime.now().strftime('%A')

    feedback_data = {
        "meal": meal,
        "rating": rating,
        "message": message,
        "weekday": weekday
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

@app.get("/get_meal_submissions")
def get_meal_submissions(
    weekday: Optional[str] = Query(None, description="Filter by day of the week (e.g., 'Monday')"),
    meal: Optional[str] = Query(None, description="Filter by meal type (e.g., 'breakfast', 'lunch')"),
    rating: Optional[int] = Query(None, ge=0, le=10, description="Filter by rating between 0 and 10")
):
    # Build query dynamically based on provided filters
    query = {}
    if weekday:
        query["weekday"] = weekday
    if meal:
        query["meal"] = meal
    if rating is not None:  # Ensure that rating=0 can be queried
        query["rating"] = rating

    # Retrieve matching documents
    results = list(meal_collection.find(query, {"_id": 0}))  # Exclude the MongoDB '_id' field from the output

    if not results:
        return {"message": "No matching meal submissions found"}

    return {"data": results}

