from typing import Annotated

from fastapi import FastAPI, Depends, Header, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from jose.exceptions import JWTClaimsError, ExpiredSignatureError
from sqlalchemy.orm import Session
from starlette.requests import Request
from starlette.responses import JSONResponse

from utils.settings import settings
from db import schemas, setup
from router import auth as auth_router, project as project_router, content as content_router
from service import auth


def start_application():
    create_app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
    setup.create_tables()
    return create_app


def get_db():
    db = setup.SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = start_application()
app.include_router(auth_router.router)
app.include_router(project_router.router)
app.include_router(content_router.router)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.middleware("http")
async def validate_token(request: Request, call_next, db: Session = Depends(get_db)):

    # There MUST be a better way to do this
    if request.url.path.rsplit('/')[1] in ['auth', 'docs', 'openapi.json']: return await call_next(request)

    auth_header = request.headers.get('Authorization')

    if auth_header is None:
        return JSONResponse(status_code=401, content="No authentication token provided")

    token = auth_header.split(" ")[1]
    try:
        payload = auth.validate_token(token, db)
        if payload.get('email') is None:
            return JSONResponse(status_code=401, content="Invalid access token. Sign up or login")
        request.state.email = payload.get('email')
    except JWTError or JWTClaimsError or ExpiredSignatureError as e:
        return JSONResponse(status_code=401, content="Invalid access token. Sign up or login")

    return await call_next(request)


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.on_event("shutdown")
def shutdown():
    db = next(get_db())
    db.close()
