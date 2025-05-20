from fastapi import APIRouter, Depends, Query
from typing import List, Optional
from sqlalchemy.orm import Session
from app.schemas.task import TaskCreate, TaskRead
from app.services.task_service import (
    get_tasks,
    create_task,
    update_task,
    delete_task,
)
from app.db.database import get_db

router = APIRouter()


@router.get("", response_model=List[TaskRead])
async def read_tasks(
    skip: int = 0,
    limit: int = 10,
    search: Optional[str] = Query(None, description="Search in title"),
    db: Session = Depends(get_db),
):
    return await get_tasks(db, skip=skip, limit=limit, search=search)


@router.post("", response_model=TaskRead)
async def create_task_endpoint(task: TaskCreate, db: Session = Depends(get_db)):
    return await create_task(db, task)


@router.put("/{task_id}", response_model=TaskRead)
async def update_task_endpoint(
    task_id: int, task: TaskCreate, db: Session = Depends(get_db)
):
    return await update_task(db, task_id, task)


@router.delete("/{task_id}")
async def delete_task_endpoint(task_id: int, db: Session = Depends(get_db)):
    return await delete_task(db, task_id)
