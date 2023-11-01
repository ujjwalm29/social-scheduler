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


def create_project(create_proj, db: Session):
    db_proj = models.Project(**create_proj.dict())
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
