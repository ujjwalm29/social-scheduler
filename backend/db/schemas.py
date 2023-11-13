from typing import List

from pydantic import BaseModel
from db import enums
from datetime import datetime


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
    live_time: datetime
    video_id: int
    thumbnail_id: int


class LinkedInDetails(BaseModel):
    text: str
    live_time: str


class Content(BaseModel):
    name: str
    platform: enums.Platform
    description: str


class ContentDetails(BaseModel):
    platform: enums.Platform
    details: YTDetails | LinkedInDetails
