FastAPI & MongoDB Backend

A FastAPI backend service integrated with MongoDB, designed to handle form submissions, feedback, and newsletter subscriptions. This API is built to be scalable, efficient, and easy to integrate with any frontend, deployed seamlessly on Render.com.

Features

Form Submissions: Collects and stores form inputs from users, including name, email, subject, and reason.

Feedback Management: Captures user feedback on meals, including meal ratings and messages.

Newsletter Subscriptions: Allows users to subscribe to a newsletter by providing their email.

Admin Control: Admin-only endpoints to manage and delete feedback data.

Flexible Querying: Allows filtering of feedback data based on date, meal, rating, and weekday.


Tech Stack

Backend Framework: FastAPI

Database: MongoDB

Deployment Platform: Render.com



---

Getting Started

Follow these instructions to set up the project on your local machine for development and testing.

Prerequisites

Ensure you have the following installed on your system:

Python 3.8+

MongoDB (local or cloud instance, such as MongoDB Atlas)

FastAPI and pydantic for building the API


Environment Variables

This project requires the following environment variables to be set:

MONGO_URI: Your MongoDB connection URI.

ADMIN_KEY: A secure admin key for accessing restricted endpoints.


You can create a .env file in the root directory and add these variables:

MONGO_URI=<your_mongodb_uri>
ADMIN_KEY=<your_admin_key>


---

Installation

1. Clone the Repository

git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name


2. Create a Virtual Environment

python3 -m venv venv
source venv/bin/activate


3. Install Dependencies

pip install -r requirements.txt


4. Set up Environment Variables

Ensure that your .env file is properly configured with the necessary values.


5. Run MongoDB Locally or Use MongoDB Atlas

If MongoDB is running locally, ensure it’s accessible. For cloud-based MongoDB, ensure your IP address is whitelisted in MongoDB Atlas.




---

Running the Application

Development Mode

To run the FastAPI application locally:

uvicorn app:app --reload

The server will start on http://127.0.0.1:8000. You can interact with the API documentation at http://127.0.0.1:8000/docs.

Production Mode

Use the following command to run without hot-reloading:

uvicorn app:app --host 0.0.0.0 --port 8000


---

API Endpoints

Example Requests

1. Submit Form Data

curl -X POST "http://127.0.0.1:8000/submit" -F "name=John Doe" -F "email=johndoe@example.com" -F "subject=Inquiry" -F "reason=Support"

2. Get Meal Submissions (Filtered)

curl -X GET "http://127.0.0.1:8000/get_meal_submissions?weekday=Monday&meal=lunch"

3. Delete Meal Feedback (Admin Only)

curl -X DELETE "http://127.0.0.1:8000/delete_meal_feedback?start_date=2024-10-01&end_date=2024-10-10" -H "Authorization: Bearer <ADMIN_KEY>"


---

Deployment on Render.com

1. Create a New Web Service on Render

Go to Render.com and log in.

Select “New” > “Web Service.”

Connect your GitHub repository to Render.



2. Environment Setup

In the Render Dashboard, navigate to Environment and add the necessary environment variables:

MONGO_URI: MongoDB connection string.

ADMIN_KEY: Admin key for protected routes.



3. Build and Start Command

For Build Command, use pip install -r requirements.txt.

For Start Command, use uvicorn app:app --host 0.0.0.0 --port 10000.



4. Deploy

Once configured, Render will deploy the service. Access the deployed API using the URL provided by Render (e.g., https://your-app-name.onrender.com).




---

License

This project is licensed under the MIT License.


---

Contributing

We welcome contributions to improve this project. Please fork the repository and create a pull request with detailed information about your changes.


---

Acknowledgments

Special thanks to the FastAPI and MongoDB communities for their extensive documentation and support.


---

This README.md should serve as a comprehensive guide for setting up, using, and deploying your FastAPI project. Let me know if you'd like additional customization or further instructions.

