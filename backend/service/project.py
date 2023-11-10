import os

from db import schemas, crud
from enum import Enum
import uuid
from utils import send_email


class ProjectRole(Enum):
    admin = 1
    editor = 2
    read_only = 3



def create_project(owner_email, create_proj: schemas.CreateProject, db):
    # create project
    db_user = crud.get_user(owner_email, db)
    db_proj = crud.create_project(db_user, create_proj, db)

    # assign owner
    crud.assign_project_member(owner_email, db_proj.project_id, ProjectRole.admin, db)

    return db_proj


def get_projects(email, db):
    db_user = crud.get_user(email, db)
    db_projects = crud.get_projects(db_user, db)

    db_roles = crud.get_project_roles(db_user, db)

    # convert to schema
    projects = []
    for db_proj in db_projects:
        role = next((role for role in db_roles if role.project_id == db_proj.project_id), None)

        if role is not None:
            projects.append(schemas.Project(**db_proj.__dict__, role=role.role))

    return projects


def check_project_owner(email, project_id, db):

    db_user = crud.get_user(email, db)
    db_proj = crud.get_project_by_id(project_id, db)

    if db_proj is None or db_proj.owner_id != db_user.user_id:
        return False

    return True


def invite_member(inviter_email, invitee_email, project_id, db):
    # create uuid
    uuid_value = uuid.uuid4()

    # make an entry in invite table
    crud.create_invite(uuid_value, inviter_email, invitee_email, project_id, db)

    # create URL with uuid
    url = "http://localhost:8000/project/invite/accept/" + str(uuid_value)

    # send email with URL
    email.send_email(os.getenv("EMAIL_ID"), invitee_email, url)

    return None


def get_invite(token, db):
    db_invite = crud.get_invite(token, db)
    return db_invite


def check_project_member(email, project_id, db):
    db_user = crud.get_user(email, db)
    db_member = crud.get_project_member(db_user, project_id, db)

    if db_member is None:
        return False

    return True


def assign_project_member(email, project_id, db):
    db_member = crud.assign_project_member(email, project_id, ProjectRole.editor, db)


def update_invite_status(token, new_status, db):
    db_invite = crud.update_invite(token, new_status, db)
