from pydantic import BaseModel, EmailStr, ValidationError, field_validator
from datetime import datetime


class SignUpModel(BaseModel):
    name: str
    surname: str
    email: EmailStr
    login: str
    password: str


class ChangePassword(BaseModel):
    old_password: str
    new_password: str


class CreateProject(BaseModel):
    name: str
    description: str
    start_time: str
    end_time: str


class UpdateProject(BaseModel):
    name: str = None
    description: str = None
    start_time: str = None
    end_time: str = None


class CreateTask(BaseModel):
    project_id: int
    description: str
    start_time: str = None
    end_time: str = None
    status_id: int = None

    @field_validator('start_time', 'end_time')
    def valid_date(cls, v):
        try:
            datetime.fromisoformat(v)
        except ValueError:
            raise ValueError("Invalid date format.")

        return v


class UpdateTask(BaseModel):
    project_id: int = None
    description: str = None
    start_time: str = None
    end_time: str = None
    status_id: int = None

    @field_validator('start_time', 'end_time')
    def valid_date(cls, v):
        try:
            datetime.fromisoformat(v)
        except ValueError:
            raise ValueError("Invalid date format.")

        return v


class CreateComment(BaseModel):
    comment_text: str


class UpdateComment(BaseModel):
    comment_text: str = None
    task_id: int = None
