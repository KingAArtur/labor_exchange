import datetime
from typing import Optional
from pydantic import BaseModel


class JobSchema(BaseModel):
    id: Optional[int] = None
    user_id: int
    title: str
    description: str
    salary_from: str
    salary_to: str
    is_active: bool = True
    created_at: datetime.datetime

    class Config:
        orm_mode = True


class JobInSchema(BaseModel):
    title: str
    description: str
    salary_from: str
    salary_to: str
