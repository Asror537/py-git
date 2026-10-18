from fastapi import FastAPI

app = FastAPI(title="Courses API")


@app.get("/")
def home():
    return {"message": "Courses API is running"}


@app.get("/courses")
def get_courses():
    return [
        {
            "id": 1,
            "name": "Python Basics",
            "duration_hours": 30
        },
        {
            "id": 2,
            "name": "SQL Fundamentals",
            "duration_hours": 20
        }
    ]