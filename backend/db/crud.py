from sqlalchemy.orm import Session

from db import schemas, models, enums



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


def assign_project_member(email, project_id, role: enums.ProjectRole, db: Session):
    user = get_user(email, db)
    db_member = models.ProjectMember(user_id=user.user_id, project_id=project_id, role=role, status="active")
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


def create_content(db_user, id, content, db):
    db_content = models.Content(**content.dict(), created_by=db_user.user_id, project_id=id)
    db.add(db_content)
    db.commit()
    return db_content


def get_content_by_id(id, db):
    db_content = db.query(models.Content).filter(models.Content.id == id).first()
    return db_content


def add_youtube_details(id, yt_details, db):
    db_yt_details = models.YTDetails(**yt_details.dict(), content_id=id)
    db.add(db_yt_details)
    db.commit()


def add_linkedin_details(id, linkedin_details, db):
    db_linkedin_details = models.LIDetails(**linkedin_details.dict(), content_id=id)
    db.add(db_linkedin_details)
    db.commit()


def add_image(content_id, key_name, email, db):
    user = get_user(email, db)
    db_image = models.Image(content_id=content_id, name=key_name, created_by=user.user_id)
    db.add(db_image)
    db.commit()


def add_video(content_id, key_name, email, status: enums.UploadStatus, db):
    user = get_user(email, db)
    db_image = models.Video(content_id=content_id, name=key_name, created_by=user.user_id, status=status)
    db.add(db_image)
    db.commit()
    return None