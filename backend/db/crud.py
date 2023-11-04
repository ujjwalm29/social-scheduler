from sqlalchemy.orm import Session

from db import schemas, models
from service.project import ProjectRole


def signup(user_create: schemas.UserCreate, hashed_password, db: Session):
    user_create.password = hashed_password
    db_user = models.User(**user_create.dict())
    db.add(db_user)
    db.commit()

    return db_user


def get_user(email: str, db: Session):
    db_user = db.query(models.User).filter(models.User.email == email).first()
    return db_user


def create_project(user, create_proj, db: Session):
    db_proj = models.Project(**create_proj.dict(), owner_id=user.user_id)
    db.add(db_proj)
    db.commit()
    db.refresh(db_proj)
    return db_proj


def assign_project_member(email, project_id, role: ProjectRole, db: Session):
    user = get_user(email, db)
    db_member = models.ProjectMember(user_id=user.user_id, project_id=project_id, role=str(role.name), status="active")
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member


def get_projects(db_user, db):
    db_projects = db.query(models.Project).filter(models.Project.owner_id == db_user.user_id).all()
    return db_projects


def get_project_by_id(proj_id, db):
    project = db.query(models.Project).filter(models.Project.project_id == proj_id).first()
    return project



def get_project_roles(db_user, db):
    db_roles = db.query(models.ProjectMember).filter(models.ProjectMember.user_id == db_user.user_id).all()
    return db_roles


def create_invite(uuid_value, inviter_email, invitee_email, project_id, db):
    db_user = get_user(inviter_email, db)
    if db_user is None:
        raise AssertionError("User does not exist")
    db_invite = models.Invite(token=uuid_value, created_by=db_user.user_id, email=invitee_email, project_id=project_id, status="pending")
    db.add(db_invite)
    db.commit()


def get_invite(token, db):
    db_invite = db.query(models.Invite).filter(models.Invite.token == token).first()
    return db_invite


def get_project_member(db_user, project_id, db):
    db_member = db.query(models.ProjectMember).filter(models.ProjectMember.user_id == db_user.user_id, models.ProjectMember.project_id == project_id).first()
    return db_member


def update_invite(token, new_status, db):
    db_invite = db.query(models.Invite).filter(models.Invite.token == token).first()
    db_invite.status = new_status
    db.commit()
