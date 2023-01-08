from models import User, Response
from schemas import ResponseInSchema
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


async def response_job(db: AsyncSession, response_scheme: ResponseInSchema, current_user: User) -> Response:
    response = Response(
        user_id=current_user.id,
        job_id=response_scheme.job_id,

        message=response_scheme.message,
    )
    db.add(response)
    await db.commit()
    await db.refresh(response)
    return response


async def get_response_by_user_id(db: AsyncSession, job_id: int) -> List[Response]:
    query = select(Response).filter(Response.job_id == job_id)
    res = await db.execute(query)
    return res.scalars().all()
