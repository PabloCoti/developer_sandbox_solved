from pydantic import BaseModel
from typing import Optional


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None


class TaskRead(TaskCreate):
    id: int

    model_config = {"from_attributes": True}
