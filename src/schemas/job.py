import datetime
from typing import Optional
from pydantic import BaseModel, validator


class JobSchema(BaseModel):
    id: Optional[int] = None
    user_id: int
    title: str
    description: str
    salary_from: int
    salary_to: int
    is_active: bool = True
    created_at: datetime.datetime

    class Config:
        orm_mode = True


class JobInSchema(BaseModel):
    title: str
    description: str
    salary_from: int
    salary_to: int

    @validator("salary_from")
    def salary_from_is_not_negative(cls, v):
        if v < 0:
            raise ValueError("Зарплата не может быть меньше нуля!")
        return v

    @validator("salary_to")
    def salary_to_is_not_less_than_from(cls, v, values, **kwargs):
        if 'salary_from' in values and v < values["salary_from"]:
            raise ValueError("Верхняя граница диапазона зарплаты не может быть меньше нижней границы!")
        return v
