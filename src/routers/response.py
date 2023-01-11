from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from schemas import ResponseSchema, ResponseInSchema
from dependencies import get_db, get_current_user
from sqlalchemy.ext.asyncio import AsyncSession
from queries import response as response_queries
from models import User, Response


router = APIRouter(prefix="/responses", tags=["responses"])


@router.get("", response_model=List[ResponseSchema])
async def get_response_by_user_id(
        job_id: int,
        db: AsyncSession = Depends(get_db),
    ):
    return await response_queries.get_response_by_user_id(db=db, job_id=job_id)


@router.post("", response_model=ResponseSchema)
async def response_job(
        response: ResponseInSchema,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)):
    if current_user.is_company:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Только соискатели могут откликаться на вакансии!")

    response = await response_queries.response_job(db=db, response_scheme=response, current_user=current_user)
    return ResponseSchema.from_orm(response)
