from sqlalchemy import Column, String, Integer, ForeignKeyConstraint, ForeignKey, func, DateTime, UniqueConstraint
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Project(Base):
    __tablename__ = "project"
    project_id: int = Column(Integer, primary_key=True)
    owner_id: int = Column(Integer, nullable=False)
    name: str = Column(String, nullable=False)
    description: str = Column(String, default="")
    time_created = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        UniqueConstraint('owner_id', 'name', name='unique_project_name'),
    )


class User(Base):
    __tablename__ = "user"
    user_id: int = Column(Integer, primary_key=True)
    email: str = Column(String, unique=True)
    name: str = Column(String, nullable=False)
    password: str = Column(String)
    profile_picture: str = Column(String)


class ProjectMember(Base):
    __tablename__ = "project_member"
    project_id: int = Column(Integer, ForeignKey("project.project_id"), primary_key=True)
    user_id: int = Column(Integer, ForeignKey("user.user_id"), primary_key=True)
    role: str = Column(String)
    status: str = Column(String)


class Content(Base):
    __tablename__ = "content"
    id: int = Column(Integer, primary_key=True)
    name: str = Column(String)
    project_id: int = Column(Integer, ForeignKey("project.project_id"))
    platform: str = Column(String)
    created_by: int = Column(Integer, ForeignKey("user.user_id"))
    description: str = Column(String)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())



class YTMeta(Base):
    __tablename__ = "yt_meta"
    id: int = Column(Integer, primary_key=True)
    content_id: int = Column(Integer, ForeignKey("content.id"))
    title: str = Column(String)
    description: str = Column(String)
    live_time: DateTime = Column(DateTime)
    video_id: int = Column(Integer, ForeignKey("video.id"))
    thumbnail_id: int = Column(Integer, ForeignKey("image.id"))


class Video(Base):
    __tablename__ = "video"
    id: int = Column(Integer, primary_key=True)
    content_id: int = Column(Integer, ForeignKey("content.id"))
    url: str = Column(String)
    time_created = Column(DateTime(timezone=True), server_default=func.now())


class Image(Base):
    __tablename__ = "image"
    id: int = Column(Integer, primary_key=True)
    content_id: int = Column(Integer, ForeignKey("content.id"))
    url: str = Column(String)
    time_created = Column(DateTime(timezone=True), server_default=func.now())


class Request(Base):
    __tablename__ = "request"
    id: int = Column(Integer, primary_key=True)
    name: str = Column(String)
    project_id: int = Column(Integer, ForeignKey("project.project_id"))
    content_id: int = Column(Integer, ForeignKey("content.id"))
    type: str = Column(String)
    status: str = Column(String)
    description: str = Column(String)
    approve_message: str = Column(String)
    created_by: int = Column(Integer, ForeignKey("user.user_id"))
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())


class Invite(Base):
    __tablename__ = "invite"
    id: int = Column(Integer, primary_key=True)
    token: str = Column(String)
    project_id: int = Column(Integer, ForeignKey("project.project_id"))
    email: str = Column(String)
    status: str = Column(String)
    created_by: int = Column(Integer, ForeignKey("user.user_id"))
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())
