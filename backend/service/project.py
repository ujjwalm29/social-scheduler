
from db import schemas, crud
from enum import Enum


class ProjectRole(Enum):
    admin = 1
    editor = 2
    read_only = 3



def create_project(owner_email, create_proj: schemas.CreateProject, db):
    # create project
    db_proj = crud.create_project(create_proj, db)

    # assign owner
    crud.assign_project_member(owner_email, db_proj.project_id, ProjectRole.admin, db)

    return db_proj
