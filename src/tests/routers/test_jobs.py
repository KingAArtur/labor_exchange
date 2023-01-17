import pytest
from routers import job_router
from fixtures.users import UserFactory
from fixtures.jobs import JobFactory
from schemas import JobInSchema, JobUpdateSchema, JobSchema
from pydantic import ValidationError
from fastapi import HTTPException
from queries import job as job_query


@pytest.mark.asyncio
async def test_read_jobs(client_app):
    # some_user = UserFactory.build()
    # sa_session.add(some_user)
    # sa_session.flush()
    #
    # n_jobs = 10
    # jobs = []
    # for _ in range(n_jobs):
    #     job = JobFactory.build()
    #     job.user_id = some_user.id
    #     jobs.append(job)
    #     sa_session.add(job)
    # sa_session.flush()

    # all_jobs = await job_query.get_all_jobs(db=sa_session)
    all_jobs = client_app.get('/jobs')
    #assert all_jobs
   # assert len(all_jobs.json()) == n_jobs
    # for job, received_job in zip(jobs, all_jobs):
    #     assert job == received_job
    #
    # skip = 2
    # limit = 5
    # all_jobs = await job_query.get_all_jobs(sa_session, skip=skip, limit=limit)
    # assert all_jobs
    # assert len(all_jobs) == limit
    # for job, received_job in zip(jobs[skip: skip + limit], all_jobs):
    #     assert job == received_job


@pytest.mark.asyncio
@pytest.mark.skip
async def test_create_job_as_company(sa_session, client_app, current_user):
    current_user.is_company = True
    sa_session.add(current_user)
    sa_session.flush()

    job = JobFactory.build()
    sa_session.add(job)
    sa_session.flush()

    created_job = job_router.post(url='/jobs', json=job)
    assert created_job
    assert created_job.title == job.title


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
