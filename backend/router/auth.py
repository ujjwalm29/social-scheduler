from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db import schemas, setup
from service import auth
from error.error import AuthException, UserExistsError

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


def get_db():
    db = setup.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/signup")
def signup(user_create: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        token = auth.signup(user_create, db)
    except UserExistsError as e:
        raise HTTPException(status_code=400, detail="User already exists. Please login")

    return {"token": token, "message": "Use token as Bearer : <token> in Authorization header"}


@router.post("/login")
def signup(user_login: schemas.UserLogin, db: Session = Depends(get_db)):
    try:
        token = auth.login(user_login, db)
    except AuthException as e:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    return {"token": token, "message": "Use token as Bearer : <token> in Authorization header"}


@router.on_event("shutdown")
def shutdown():
    db = next(get_db())
    db.close()

