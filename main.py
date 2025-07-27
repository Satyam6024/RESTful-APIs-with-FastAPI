from typing import Union
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException

app = FastAPI()

tasks_db = [] #sql excel register 


class TaskCreate(BaseModel):
    title: str
    description:str
    owner: str

class TaskResponse(TaskCreate):
    id: int
    is_completed: bool

@app.get('/')
def home():
    return {"message": "Welcome to the Task Management API"}

@app.post('/addtask', response_model=TaskResponse )
def add_task(task: TaskCreate):
    task_dict = task.dict()
    task_dict['id'] = len(tasks_db) + 1
    task_dict['is_completed'] = False
    tasks_db.append(task_dict)
    return task_dict

@app.get('/gettask')
def get_all_tasks():
    return tasks_db

@app.get('/gettask/{owner}')
def get_task_by_owner(owner: str):
    for task in tasks_db:
        if task['owner'] == owner:
            return task
    raise HTTPException(status_code=404, detail="Task not found")

