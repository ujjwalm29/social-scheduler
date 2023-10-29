from sqlalchemy.orm import Session

from db import schemas, models


def signup(user_create: schemas.UserCreate, hashed_password, db: Session):
    user_create.password = hashed_password
    db_user = models.User(**user_create.dict())
    db.add(db_user)
    db.commit()

    return db_user


def login(user_login: schemas.UserLogin, db: Session):
    db_user = db.query(models.User).filter(models.User.email == user_login.email).first()
    return db_user
