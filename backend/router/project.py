from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.requests import Request

from db import schemas, setup
from db.schemas import CreateProject
from service import project

router = APIRouter(
    prefix="/project",
    tags=["project"],
)


def get_db():
    db = setup.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/create")
async def create_project(request: Request, create_proj: CreateProject, db: Session = Depends(get_db)):
    new_project = project.create_project(request.state.email, create_proj, db)

    return {"project": new_project, "message": "Project created successfully"}


@router.on_event("shutdown")
def shutdown():
    db = next(get_db())
    db.close()
