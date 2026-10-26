
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI(title="Courses API")


class CourseCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    duration_hours: int = Field(gt=0)
    description: str = Field(min_length=3, max_length=500)

class CourseUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2, max_length=100)
    duration_hours: Optional[int] = Field(default=None, gt=0)
    description: Optional[str] = Field(default=None, min_length=5, max_length=500)

courses = [
    {
        "id": 1,
        "name": "Python Basics",
        "duration_hours": 30,
        "description": "Introduction to Python"
    },
    {
        "id": 2,
        "name": "SQL Fundamentals",
        "duration_hours": 20,
        "description": "Introduction to SQL"
    }
]


@app.get("/")
def home():
    return {"message": "Courses API is running"}


@app.get("/courses")
def get_courses(
    min_duration: Optional[int] = None,
    max_duration: Optional[int] = None
):
    if min_duration is not None and max_duration is not None and min_duration > max_duration:
        raise  HTTPException(status_code=400, detail='Wrong options written')
    else:
        temp_courses = []

        for course in courses:
            duration = course["duration_hours"]

            if min_duration is not None and duration < min_duration:
                continue

            if max_duration is not None and duration > max_duration:
                continue

            temp_courses.append(course)

        return temp_courses


@app.get("/courses/{id}")
def get_course(id: int):
    for i in courses:
        if i['id'] == id:
            return i
    raise HTTPException(status_code=404, detail="Course not found")

@app.post("/courses", status_code=201)
def create_course(course: CourseCreate):
    new_id = max((item["id"] for item in courses), default=0) + 1

    new_course = {
        "id": new_id,
        **course.model_dump()
    }

    courses.append(new_course)
    return new_course


@app.patch("/courses/{id}")
def update_course(id: int, course_update: CourseUpdate):

    for course in courses:
        if course["id"] == id:
   
            update_data = course_update.model_dump(exclude_unset=True)


            if not update_data:
                raise HTTPException(status_code=400, detail="Request body cannot be empty")

       
            course.update(update_data)

            return course


    raise HTTPException(status_code=404, detail="Course not found")


@app.delete("/courses/{id}", status_code=204)
def delete_course(id: int):
    for course in courses:
        if course["id"] == id:
            courses.remove(course)
            return

    raise HTTPException(status_code=404, detail="Course not found")
