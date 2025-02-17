from models import Job, User
from schemas import JobInSchema
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


async def create_job(db: AsyncSession, job_schema: JobInSchema, current_user: User) -> Job:
    job = Job(
        user_id=current_user.id,
        title=job_schema.title,
        description=job_schema.description,
        salary_from=job_schema.salary_from,
        salary_to=job_schema.salary_to,
    )
    db.add(job)
    await db.commit()
    await db.refresh(job)
    return job


async def get_all_jobs(db: AsyncSession, limit: int = 100, skip: int = 0) -> List[Job]:
    query = select(Job).limit(limit).offset(skip)
    res = await db.execute(query)
    return res.scalars().all()


async def get_job_by_id(db: AsyncSession, job_id: int) -> Optional[Job]:
    query = select(Job).where(Job.id == job_id).limit(1)
    res = await db.execute(query)
    return res.scalars().first()


async def delete_job(db: AsyncSession, job: Job) -> Job:
    await db.delete(job)
    await db.commit()
    return job


async def update_job(db: AsyncSession, job: Job) -> Job:
    db.add(job)
    await db.commit()
    await db.refresh(job)
    return job
