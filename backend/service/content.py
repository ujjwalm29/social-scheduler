from db import crud, schemas, models
from utils import upload_media


def create_content(email, id, content, db):
    db_user = crud.get_user(email, db)
    db_content = crud.create_content(db_user, id, content, db)
    return db_content.id


def get_project_of_content(id, db):
    db_content = crud.get_content_by_id(id, db)

    if db_content is not None:
        return db_content.project_id


def add_content_details(c_id, details: schemas.ContentDetails, db):
    if details.platform == "youtube":
        crud.add_youtube_details(c_id, details.details, db)
    elif details.platform == "youtube":
        crud.add_linkedin_details(c_id, details.details, db)


def create_signed_url(email, c_id, image, db):
    url = upload_media.generate_image_presigned_url(image, email, c_id, db)
    return url
