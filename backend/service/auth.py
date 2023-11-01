import os
from datetime import timedelta, datetime

from jose import jwt
from sqlalchemy.orm import Session

from db import crud, schemas
from passlib.context import CryptContext
from error.error import AuthException, UserExistsError

ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def signup(user_create: schemas.UserCreate, db: Session):
    db_user = crud.get_user(user_create.email, db)
    if db_user is not None:
        raise UserExistsError()
    hash_pwd = pwd_context.hash(user_create.password)
    db_user = crud.signup(user_create, hash_pwd, db)

    return create_access_token({"email": db_user.email, "name": db_user.name})


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, os.getenv("SECRET_KEY"), algorithm=ALGORITHM)
    return encoded_jwt


def login(user_login: schemas.UserLogin, db: Session):
    db_user = crud.get_user(user_login.email, db)
    if db_user is None:
        raise AuthException()
    if not verify_password(user_login.password, db_user.password):
        raise AuthException()
    return create_access_token({"email": db_user.email, "name": db_user.name})


def validate_token(token: str, db: Session):
    payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=[ALGORITHM])
    return payload


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
