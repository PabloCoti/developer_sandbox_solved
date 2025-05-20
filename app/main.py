from fastapi import FastAPI
from app.models import Task
from app.db import engine, Base
from app.api.tasks import router as tasks_router

app = FastAPI()
app.include_router(tasks_router, prefix="/tasks")


@app.on_event("startup")
async def startup():
    from sqlalchemy.orm import Session

    Base.metadata.create_all(bind=engine)

    with Session(engine) as session:
        for i in range(1, 101):
            task = Task(title=f"Task {i}", description=f"Description for task {i}")
            session.add(task)

        session.commit()
