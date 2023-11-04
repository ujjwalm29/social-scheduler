from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from starlette.requests import Request
from starlette.responses import JSONResponse

from db import schemas, setup
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
async def create_project(request: Request, create_proj: schemas.CreateProject, db: Session = Depends(get_db)):
    try:
        new_project = project.create_project(request.state.email, create_proj, db)
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail="Project already exists. Please choose a different name.")

    return JSONResponse(status_code=201, content={"project_id": new_project.project_id})


@router.get("", response_model=List[schemas.Project])
async def get_projects(request: Request, db: Session = Depends(get_db)):
    return project.get_projects(request.state.email, db)


@router.post("/invite", status_code=201)
async def invite_members(request: Request, invite: schemas.ProjectInvite, db: Session = Depends(get_db)):
    # check if requestor is owner
    if project.check_project_owner(request.state.email, invite.project_id, db) is False:
        raise HTTPException(status_code=401, detail="You are not authorized to invite members to this project")

    # for each user email, generate uuid, store in db, send email invite
    for email in invite.emails:
        project.invite_member(request.state.email, email, invite.project_id, db)


@router.get("/invite/accept/{token}", status_code=200)
async def accept_invite(request: Request, token: str, db: Session = Depends(get_db)):
    # check if token exists
    invite = project.get_invite(token, db)
    if invite is None:
        raise HTTPException(status_code=404, detail="Invite not found")

    # check if invite is pending
    if invite.status != "pending":
        raise HTTPException(status_code=400, detail="Invite has already been accepted")

    # check if user already has access to project
    if project.check_project_member(invite.email, invite.project_id, db):
        raise HTTPException(status_code=400, detail="User already has access to project")

    # add user to project
    project.assign_project_member(invite.email, invite.project_id, db)

    # update invite status
    project.update_invite_status(token, "accepted", db)

    return JSONResponse(status_code=200, content={"msg": "Invite accepted"})



@router.on_event("shutdown")
def shutdown():
    db = next(get_db())
    db.close()
