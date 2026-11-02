
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()
class TaskCreate(BaseModel):
    title: str


# Sample tasks stored in memory
tasks = [
    {"id": 1, "title": "Learn Python", "done": False},
    {"id": 2, "title": "Build my first API", "done": False},
    {"id": 3, "title": "Practice FastAPI", "done": True},
]


@app.get("/")
def home():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/tasks")
def get_tasks():
    return tasks


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task

        raise HTTPException(
            status_code=404,
            detail={"error": f"Task {task_id} not found"}
        )


    # Create a new task

@app.post("/tasks", status_code=201)
def create_task(task_data: TaskCreate):
    title = task_data.title.strip()

    if not title:
        raise HTTPException(
            status_code=400,
            detail={"error": "Title is required and cannot be empty"}
        )

    next_id = max((task["id"] for task in tasks), default=0) + 1

    new_task = {
        "id": next_id,
        "title": title,
        "done": False
    }

    tasks.append(new_task)
    return new_task
