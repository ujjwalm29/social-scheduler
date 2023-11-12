from enum import Enum


class Platform(str, Enum):
    youtube = "youtube"
    instagram = "instagram"
    tiktok = "tiktok"
    facebook = "facebook"
    linkedin = "linkedin"


class ProjectRole(str, Enum):
    admin = "admin"
    editor = "editor"
    read_only = "read_only"
