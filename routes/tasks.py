from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from models import UserModel
from schema import TaskCreate, Task
from crud import create_task, get_tasks, get_task, update_task, delete_task
from database import get_db
from security import get_current_user

router = APIRouter()

# Create a new task
@router.post("/tasks/", response_model=Task)
async def create_new_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    new_task = create_task(db, task, current_user.id)
    if new_task is None:
        raise HTTPException(status_code=400, detail="Task creation failed.")
    return new_task

# Get all tasks for the current user
@router.get("/tasks/", response_model=List[Task])
async def read_user_tasks(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    tasks = get_tasks(db, current_user.id)
    return tasks

# Get a specific task by ID
@router.get("/tasks/{task_id}", response_model=Task)
async def read_task_by_id(
    task_id: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    task = get_task(db, task_id, current_user.id)
    if task is None:
        print(f"Task with ID {task_id} not found for user {current_user.id}.")
        raise HTTPException(status_code=404, detail="Task not found")
    return task

# Update a task
@router.put("/tasks/{task_id}", response_model=Task)
async def update_existing_task(
    task_id: str,
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    updated_task = update_task(db, task_id, current_user.id, task)
    if updated_task is None:
        print(f"Failed to update task with ID {task_id}. Task not found for user {current_user.id}.")
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task

# Delete a task
@router.delete("/tasks/{task_id}", response_model=dict)
async def delete_task_by_id(
    task_id: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    deleted_task = delete_task(db, task_id, current_user.id)
    if deleted_task is None:
        print(f"Failed to delete task with ID {task_id}. Task not found for user {current_user.id}.")
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted successfully"}
