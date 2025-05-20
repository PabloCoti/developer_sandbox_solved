import time
import json
from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskRead
from app.cache.redis_client import redis


def serialize_tasks(tasks):
    return json.dumps(
        [{"id": t.id, "title": t.title, "description": t.description} for t in tasks]
    )


def deserialize_tasks(data):
    return [TaskRead(**item) for item in json.loads(data)]


async def get_tasks(
    db: Session, skip: int = 0, limit: int = 999, search: Optional[str] = None
):
    cache_key = f"tasks:{skip}:{limit}:{search or ''}"
    start_time = time.time()
    cached = await redis.get(cache_key)

    if cached:
        print(
            f"[CACHE] GET /tasks - Time: {time.time() - start_time:.4f}s (from cache)"
        )

        return deserialize_tasks(cached)

    query = db.query(Task)

    if search:
        query = query.filter(Task.title.contains(search))

    tasks = query.offset(skip).limit(limit).all()
    result = [TaskRead.model_validate(t) for t in tasks]

    await redis.set(cache_key, serialize_tasks(result), ex=60)

    print(f"[DB] GET /tasks - Time: {time.time() - start_time:.4f}s (from DB)")
    return result


async def create_task(db: Session, task: TaskCreate):
    db_task = Task(title=task.title, description=task.description)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    await redis.flushdb()

    return TaskRead.model_validate(db_task)


async def update_task(db: Session, task_id: int, task: TaskCreate):
    db_task = db.query(Task).filter(Task.id == task_id).first()

    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    db_task.title = task.title
    db_task.description = task.description
    db.commit()
    db.refresh(db_task)

    await redis.flushdb()

    return TaskRead.model_validate(db_task)


async def delete_task(db: Session, task_id: int):
    db_task = db.query(Task).filter(Task.id == task_id).first()

    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(db_task)
    db.commit()

    await redis.flushdb()

    return {"ok": True}
