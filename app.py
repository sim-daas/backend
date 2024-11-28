from fastapi import FastAPI, Form, Query, HTTPException, Depends
from pymongo import MongoClient
from pydantic import BaseModel, EmailStr
import os
from datetime import datetime
from typing import Optional
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from any IP address or domain
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# MongoDB client setup (replace with your MongoDB URI)
MONGO_URI = os.getenv('MONGO_URI')
client = MongoClient(MONGO_URI)
db = client["your_database"]
collection = db["submissions"]
meal_collection = db["meal_feedback"]
contactus = db["contactus"]
newsletter_emails = db["subscribed_emails"]
admins_collection = db["admins"]
ADMIN_KEY = os.getenv('ADMIN_KEY')


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
    current_date = datetime.now().strftime("%Y-%m-%d")  # e.g., "2024-10-27"
    # Create a dictionary to save in MongoDB
    submission_data = {
        "name": name,
        "email": email,
        "subject": subject,
        "reason": reason,
        "date": current_date
    }

    # Insert into MongoDB
    result = collection.insert_one(submission_data)
    return {"message": "Submission successful", "id": str(result.inserted_id)}


class MealFeedback(BaseModel):
    meal: str
    rating: int
    message: str


@app.post("/postcontactus")
def submit_meal(
    name: str = Form(...),
    phone: str = Form(...),
    email: str = Form(...),
    subject: str = Form(...),
    message: str = Form(...)
):

    current_date = datetime.now().strftime("%Y-%m-%d")  # e.g., "2024-10-27"

    feedback_data = {
        "name": name,
        "phone": phone,
        "email": email,
        "subject": subject,
        "message": message,
        "date": current_date
    }
    result = contactus.insert_one(feedback_data)
    return {"message": "Feedback submitted successfully", "id": str(result.inserted_id)}


@app.post("/submit_meal")
def submit_meal(
    meal: str = Form(...),
    rating: int = Form(...),
    message: str = Form(...)
):

    weekday = datetime.now().strftime('%A')
    current_date = datetime.now().strftime("%Y-%m-%d")  # e.g., "2024-10-27"

    feedback_data = {
        "meal": meal,
        "rating": rating,
        "message": message,
        "weekday": weekday,
        "date": current_date
    }
    result = meal_collection.insert_one(feedback_data)
    return {"message": "Feedback submitted successfully", "id": str(result.inserted_id)}


@app.post("/getemails")
def submit_meal(
    email: str = Form(...)
):
    feedback_data = {
        "email": email,
    }
    result = newsletter_emails.insert_one(feedback_data)
    return {"message": "Feedback submitted successfully", "id": str(result.inserted_id)}


@app.get("/getmessages")
def get_messages():
    messages = collection.find({}, {"_id": 0})
    # Convert cursor to list of dictionaries
    message_list = [jsonable_encoder(message) for message in messages]
    return {"messages": message_list}


@app.get("/subcemails")
def get_subscribed_emails():
    emails = newsletter_emails.find({}, {"_id": 0})
    # Convert cursor to list of dictionaries
    email_list = [jsonable_encoder(email) for email in emails]
    return {"emails": email_list}

@app.get("/admin_login")
def login_admin(
    email: str = Query(..., description="Admin's email"),
    password: str = Query(..., description="Admin's password")
):
    # Query the admins collection for the given email and password
    admin = admins_collection.find_one({"email": email, "password": password})
    
    if admin:
        return {"success": True, "message": "Login successful"}
    else:
        return {"success": False, "message": "Invalid email or password"}

@app.get("/average_ratings")
def get_average_rating(meal: Optional[str] = None):
    current_date = datetime.now().strftime("%Y-%m-%d")  # Get current date in YYYY-MM-DD format

    if meal:  # If a specific meal is provided
        # Build the query to filter by date and meal
        query = {"date": current_date, "meal": meal}
        
        # Retrieve ratings for the specified meal
        ratings = meal_collection.find(query, {"rating": 1})
        ratings_list = [entry["rating"] for entry in ratings]
        
        if not ratings_list:
            raise HTTPException(status_code=404, detail=f"No ratings found for meal: {meal} on {current_date}")
        
        average_rating = round(sum(ratings_list) / len(ratings_list), 1)
        return {"meal": meal, "average_rating": average_rating, "date": current_date}
    
    # If no specific meal is provided, calculate averages for all meals
    meal_types = ["breakfast", "lunch", "snacks", "dinner"]
    averages = {}
    
    for meal_type in meal_types:
        query = {"date": current_date, "meal": meal_type}
        ratings = meal_collection.find(query, {"rating": 1})
        ratings_list = [entry["rating"] for entry in ratings]
        
        if ratings_list:  # Calculate average if ratings exist
            averages[meal_type] = round(sum(ratings_list) / len(ratings_list), 1)
        else:  # No ratings for this meal type
            averages[meal_type] = None
    
    return {"average_ratings": averages, "date": current_date}

@app.get("/get_meal_submissions")
def get_meal_submissions(
    weekday: Optional[str] = Query(
        None, description="Filter by day of the week (e.g., 'Monday')"),
    meal: Optional[str] = Query(
        None, description="Filter by meal type (e.g., 'breakfast', 'lunch')"),
    rating: Optional[int] = Query(
        None, ge=0, le=10, description="Filter by rating between 0 and 10")
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
    # Exclude the MongoDB '_id' field from the output
    results = list(meal_collection.find(query, {"_id": 0}))

    if not results:
        return {"message": "No matching meal submissions found"}

    return {"data": results}


def is_admin(auth_key: str):
    if auth_key != ADMIN_KEY:
        raise HTTPException(status_code=403, detail="Unauthorized access")


@app.delete("/delete_meal_feedback")
def delete_meal_feedback(
    auth_key: str = Depends(is_admin),
    start_date: Optional[str] = Query(
        None, description="Start date in YYYY-MM-DD format"),
    end_date: Optional[str] = Query(
        None, description="End date in YYYY-MM-DD format")
):
    # Check if both start_date and end_date are provided
    if start_date and end_date:
        # Validate date format and build query
        try:
            start = datetime.strptime(start_date, "%Y-%m-%d")
            end = datetime.strptime(end_date, "%Y-%m-%d")
        except ValueError:
            raise HTTPException(
                status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")

        # Create query to delete entries within the specified date range
        query = {"date": {"$gte": start_date, "$lte": end_date}}
    else:
        # No date range provided, delete all documents
        query = {}

    # Perform deletion
    result = meal_collection.delete_many(query)
    return {"message": f"Deleted {result.deleted_count} entries from the meal_feedback collection"}
