import pytest

from fixtures.users import UserFactory
from fixtures.jobs import JobFactory
from schemas import JobInSchema, JobUpdateSchema
from fastapi import status


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

    created_job = await client_app.post(url='/jobs', json=job_schema.dict())

    assert created_job.json()["title"] == job.title


@pytest.mark.asyncio
async def test_create_job_as_not_company(sa_session, client_app, current_user):
    current_user.is_company = False
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

    created_job = await client_app.post(url='/jobs', json=job_schema.dict())

    assert created_job.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_delete_job(sa_session, client_app, current_user):
    job = JobFactory.build(salary_from=10, salary_to=20)
    job.user_id = current_user.id
    sa_session.add(job)
    sa_session.flush()
    job_id = job.id

    deleted_job = await client_app.delete(url=f'/jobs?job_id={job_id}')

    assert deleted_job.json()['id'] == job_id

    deleted_job = await client_app.delete(url=f'/jobs?job_id={job_id}')

    # TODO: этого не должно здесь быть!
    sa_session.expunge(job)

    assert deleted_job.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_delete_job_other_user(sa_session, client_app):
    other_user = UserFactory.build()
    sa_session.add(other_user)
    sa_session.flush()

    job = JobFactory.build()
    job.user_id = other_user.id
    sa_session.add(job)
    sa_session.flush()

    deleted_job = await client_app.delete(url=f'/jobs?job_id={job.id}')

    assert deleted_job.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_update_job(sa_session, client_app, current_user):
    job = JobFactory.build()
    job.user_id = current_user.id
    sa_session.add(job)
    sa_session.flush()

    job_update = JobUpdateSchema(
        title=job.title + '[updated]',
        is_active=not job.is_active
    )

    to_send = job_update.dict(exclude_unset=True)

    updated_job = await client_app.put(url=f'/jobs?job_id={job.id}', json=to_send)
    assert updated_job
    assert updated_job.json()['id'] == job.id


@pytest.mark.asyncio
async def test_update_job_other_user(sa_session, client_app, current_user):
    other_user = UserFactory.build()
    sa_session.add(other_user)
    sa_session.flush()

    job = JobFactory.build()
    job.user_id = other_user.id
    sa_session.add(job)
    sa_session.flush()

    job_update = JobUpdateSchema(
        title=job.title + '[updated]',
        is_active=not job.is_active
    )

    updated_job = await client_app.put(url=f'/jobs?job_id={job.id}', json=job_update.dict())
    assert updated_job.status_code == status.HTTP_403_FORBIDDEN
