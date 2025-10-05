from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from schemas.task import TaskCreate, TaskOut
from models.task import Task
from core.database import get_db
from utils.response import api_json_response_format  # Adjust path if needed

router = APIRouter()

@router.post("/")
def create_task(task_in: TaskCreate, db: Session = Depends(get_db)):
    try:
        task = Task(**task_in.model_dump())
        db.add(task)
        db.commit()
        db.refresh(task)
        return api_json_response_format(True, "Task created successfully.", 201, TaskOut.model_validate(task).model_dump())
    except Exception as e:
        return api_json_response_format(False, f"Error creating task: {e}", 500, {})

@router.get("/")
def get_tasks(db: Session = Depends(get_db)):
    try:
        tasks = db.query(Task).all()
        data = [TaskOut.model_validate(t).model_dump() for t in tasks]
        return api_json_response_format(True, "Tasks retrieved successfully.", 200, data)
    except Exception as e:
        return api_json_response_format(False, f"Error retrieving tasks: {e}", 500, {})

@router.get("/{task_id}")
def get_task(task_id: int, db: Session = Depends(get_db)):
    try:
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task:
            return api_json_response_format(False, "Task not found", 404, {})
        return api_json_response_format(True, "Task retrieved successfully.", 200, TaskOut.model_validate(task).model_dump())
    except Exception as e:
        return api_json_response_format(False, f"Error retrieving task: {e}", 500, {})

@router.put("/{task_id}")
def update_task(task_id: int, task_in: TaskCreate, db: Session = Depends(get_db)):
    try:
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task:
            return api_json_response_format(False, "Task not found", 404, {})
        for key, value in task_in.model_dump().items():
            setattr(task, key, value)
        db.commit()
        db.refresh(task)
        return api_json_response_format(True, "Task updated successfully.", 200, TaskOut.model_validate(task).model_dump())
    except Exception as e:
        return api_json_response_format(False, f"Error updating task: {e}", 500, {})

@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    try:
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task:
            return api_json_response_format(False, "Task not found", 404, {})
        db.delete(task)
        db.commit()
        return api_json_response_format(True, "Task deleted successfully.", 200, {})
    except Exception as e:
        return api_json_response_format(False, f"Error deleting task: {e}", 500, {})