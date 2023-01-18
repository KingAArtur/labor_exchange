import pytest

from core.security import create_access_token
from routers import job_router
from fixtures.users import UserFactory
from fixtures.jobs import JobFactory
from schemas import JobInSchema, TokenSchema
from fastapi import HTTPException


@pytest.mark.asyncio
async def test_read_jobs(sa_session, client_app):
    some_user = UserFactory.build()
    sa_session.add(some_user)
    sa_session.flush()

    n_jobs = 10
    jobs = []
    for _ in range(n_jobs):
        job = JobFactory.build()
        job.user_id = some_user.id
        jobs.append(job)
        sa_session.add(job)
    sa_session.flush()

    all_jobs = await client_app.get('/jobs')
    assert all_jobs
    assert len(all_jobs.json()) == n_jobs


@pytest.mark.asyncio
async def test_create_job_as_company(sa_session, client_app, current_user):
    current_user.is_company = True
    sa_session.add(current_user)
    sa_session.flush()

    job = JobFactory.build(salary_from=10, salary_to=20)
    sa_session.add(job)
    sa_session.flush()
    job_schema = JobInSchema(
        title=job.title,
        description=job.description,
        salary_from=job.salary_from,
        salary_to=job.salary_to
    )

    token = TokenSchema(
        access_token=create_access_token({"sub": current_user.email}),
        token_type="Bearer"
    )

    client_app.headers["Authorization"] = f"Bearer {token.access_token}"

    created_job = await client_app.post(url='/jobs', json=job_schema.dict())
    assert created_job
    assert created_job.json()["title"] == job.title


@pytest.mark.asyncio
@pytest.mark.skip
async def test_create_job_as_not_company(sa_session, client_app, current_user):
    current_user.is_company = False
    sa_session.add(current_user)
    sa_session.flush()

    job = JobFactory.build()
    sa_session.add(job)
    sa_session.flush()

    with pytest.raises(HTTPException):
        created_job = job_router.post(url='/jobs', json=job)


@pytest.mark.asyncio
@pytest.mark.skip
async def test_delete_job(sa_session, client_app, current_user):
    job = JobFactory.build()
    job.user_id = current_user.id
    sa_session.add(job)
    sa_session.flush()

    deleted_job = job_router.delete(url=f'/jobs?job_id={job.id}')
    assert deleted_job


@pytest.mark.asyncio
@pytest.mark.skip
async def test_delete_job_other_user(sa_session, client_app, current_user):
    other_user = UserFactory.build()
    sa_session.add(other_user)
    sa_session.flush()

    job = JobFactory.build()
    job.user_id = other_user.id
    sa_session.add(job)
    sa_session.flush()

    with pytest.raises(HTTPException):
        deleted_job = job_router.delete(url=f'/jobs?job_id={job.id}')


@pytest.mark.asyncio
@pytest.mark.skip
async def test_update_job(sa_session, client_app, current_user):
    job = JobFactory.build()
    job.user_id = current_user.id
    sa_session.add(job)
    sa_session.flush()

    job.title += '[updated]'
    job.is_active = not job.is_active

    updated_job = job_router.post(url=f'/jobs?job_id={job.id}', json=job)
    assert updated_job
    assert updated_job.id == job.id


@pytest.mark.asyncio
@pytest.mark.skip
async def test_update_job_other_user(sa_session, client_app, current_user):
    other_user = UserFactory.build()
    sa_session.add(other_user)
    sa_session.flush()

    job = JobFactory.build()
    job.user_id = other_user.id
    sa_session.add(job)
    sa_session.flush()

    job.title += '[updated]'
    job.is_active = not job.is_active

    updated_job = job_router.post(url=f'/jobs?job_id={job.id}', json=job)
    assert updated_job
    assert updated_job.id == job.id
