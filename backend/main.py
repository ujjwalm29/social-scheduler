from fastapi import FastAPI

from utils.settings import settings
from db import schemas, setup
from router.auth import router


def start_application():
    create_app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
    setup.create_tables()
    return create_app


app = start_application()
app.include_router(router)



@app.get("/")
async def root():
    return {"message": "Hello World"}
