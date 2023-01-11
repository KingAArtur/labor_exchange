from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from schemas import JobSchema, JobInSchema
from dependencies import get_db, get_current_user
from sqlalchemy.ext.asyncio import AsyncSession
from queries import job as job_queries
from models import Job, User


router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.get("", response_model=List[JobSchema])
async def read_jobs(
        db: AsyncSession = Depends(get_db),
        limit: int = 100,
        skip: int = 0):
    return await job_queries.get_all_jobs(db=db, limit=limit, skip=skip)


@router.post("", response_model=JobSchema)
async def create_job(
        job: JobInSchema,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)):
    job = await job_queries.create_job(db=db, job_schema=job, current_user=current_user)
    return JobSchema.from_orm(job)


@router.delete("", response_model=JobSchema)
async def delete_job(
        job_id: int,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)):
    old_job = await job_queries.get_job_by_id(db=db, job_id=job_id)

    if old_job is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Вакансия не найдена.")

    if old_job.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Нельзя удалять чужую вакансию!")

    deleted_job = await job_queries.delete_job(db=db, job=old_job)

    return JobSchema.from_orm(deleted_job)
