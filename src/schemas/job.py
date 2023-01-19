import datetime
from typing import Optional
from pydantic import BaseModel, validator


def salary_is_not_negative(salary: int):
    if salary is not None:
        if salary < 0:
            raise ValueError("Зарплата не может быть меньше нуля!")
    return salary


def salary_to_is_not_less_than_from(salary, values, **kwargs):
    if salary is not None:
        if 'salary_from' in values and values["salary_from"] is not None and salary < values["salary_from"]:
            raise ValueError("Верхняя граница диапазона зарплаты не может быть меньше нижней границы!")
    return salary


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
        validate_assignment = True

    _salary_from_is_not_negative = validator('salary_from', allow_reuse=True)(salary_is_not_negative)
    _salary_to_is_not_less_than_from = validator('salary_to', allow_reuse=True)(salary_to_is_not_less_than_from)


class JobUpdateSchema(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    salary_from: Optional[int] = None
    salary_to: Optional[int] = None
    is_active: Optional[bool] = None

    _salary_from_is_not_negative = validator('salary_from', allow_reuse=True)(salary_is_not_negative)
    _salary_to_is_not_less_than_from = validator('salary_to', allow_reuse=True)(salary_to_is_not_less_than_from)


class JobInSchema(BaseModel):
    title: str
    description: str
    salary_from: int
    salary_to: int

    _salary_from_is_not_negative = validator('salary_from', allow_reuse=True)(salary_is_not_negative)
    _salary_to_is_not_less_than_from = validator('salary_to', allow_reuse=True)(salary_to_is_not_less_than_from)
