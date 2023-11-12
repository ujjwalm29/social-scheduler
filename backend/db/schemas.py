from typing import List

from pydantic import BaseModel
from db import enums


class UserCreate(BaseModel):
    email: str
    name: str
    password: str
    profile_picture: str | None


class UserLogin(BaseModel):
    email: str
    password: str


class CreateProject(BaseModel):
    name: str
    description: str


class Project(BaseModel):
    project_id: int
    role: str
    name: str
    description: str


class ProjectInvite(BaseModel):
    project_id: int
    emails: List[str]


class YTDetails(BaseModel):
    title: str
    description: str
    live_time: str
    video_id: str
    thumbnail_id: str


class Content(BaseModel):
    name: str
    platform: enums.Platform
    description: str



