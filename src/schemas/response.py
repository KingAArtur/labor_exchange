from typing import Optional
from pydantic import BaseModel


class ResponseSchema(BaseModel):
    id: Optional[str] = None
    user_id: int
    job_id: int

    message: str

    class Config:
        orm_mode = True


class ResponseInSchema(BaseModel):
    job_id: int
    message: str
