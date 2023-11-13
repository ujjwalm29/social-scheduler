from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from starlette.requests import Request
from starlette.responses import JSONResponse

from db import schemas, setup
from service import project, content as content_service


router = APIRouter(
    prefix="/content/{c_id}",
    tags=["content"],
)


def get_db():
    db = setup.SessionLocal()
    try:
        yield db
    finally:
        db.close()


def validate_id(request: Request, c_id: int, db: Session = Depends(get_db)):
    # get project of content
    project_id = content_service.get_project_of_content(c_id, db)

    # check if this user is admin or editor of the project that this content belongs to
    if project.check_project_member_role(request.state.email, project_id, db) is False:
        raise HTTPException(status_code=401, detail="You are not authorized to access this content")

    return c_id


@router.post("/details", status_code=201)
async def content_details(request: Request, details: schemas.ContentDetails, c_id: int = Depends(validate_id), db: Session = Depends(get_db)):
    content_service.add_content_details(c_id, details, db)


@router.post("/upload/image", status_code=201)
async def upload_image(request: Request, image: str, c_id: int = Depends(validate_id), db: Session = Depends(get_db)):
    url = content_service.create_signed_url(request.state.email, c_id, image, db)
    return JSONResponse(status_code=201, content={"presigned_url": f"{url}"})


def get_db():
    db = setup.SessionLocal()
    try:
        yield db
    finally:
        db.close()
