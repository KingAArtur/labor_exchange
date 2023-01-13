import pytest
from queries import job as job_query
from fixtures.users import UserFactory
from fixtures.jobs import JobFactory
from schemas import JobInSchema, JobUpdateSchema
from pydantic import ValidationError


@pytest.mark.asyncio
async def test_create_job_negative_salary():
    with pytest.raises(ValidationError):
        job = JobInSchema(
            title='superwork',
            description='you gonna pay me instead',
            salary_from=-500,
            salary_to=-100
        )


@pytest.mark.asyncio
async def test_create_job_from_bigger_to():
    with pytest.raises(ValidationError):
        job = JobInSchema(
            title='superwork',
            description='500 > 100???',
            salary_from=500,
            salary_to=100
        )


@pytest.mark.asyncio
async def test_update_job_negative_salary():
    with pytest.raises(ValidationError):
        job = JobUpdateSchema(
            title='superwork',
            description='you gonna pay me instead',
            salary_from=-500,
            salary_to=-100,
            is_active=False
        )


@pytest.mark.asyncio
async def test_update_job_from_bigger_to():
    with pytest.raises(ValidationError):
        job = JobUpdateSchema(
            title='superwork',
            description='500 > 100???',
            salary_from=500,
            salary_to=100,
            is_active=False
        )


@pytest.mark.asyncio
async def test_create_job(sa_session, current_user):
    job = JobInSchema(
        title='correct_work',
        description='holy moly this is correct?',
        salary_from=5000,
        salary_to=10000
    )
    new_job = await job_query.create_job(sa_session, job_schema=job, current_user=current_user)

    assert new_job is not None
    assert new_job.title == job.title
    assert new_job.user_id == current_user.id


@pytest.mark.asyncio
async def test_update_job(sa_session, current_user):
    job = JobFactory.build()
    job.user_id = current_user.id
    sa_session.add(job)
    sa_session.flush()

    job.title += '[updated!]'
    job.salary_to += 10000
    updated_job = await job_query.update_job(sa_session, job=job)

    assert job.id == updated_job.id
    assert job.salary_from == updated_job.salary_from


@pytest.mark.asyncio
async def test_get_all_jobs(sa_session):
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

    all_jobs = await job_query.get_all_jobs(sa_session)
    assert all_jobs
    assert len(all_jobs) == n_jobs
    for job, received_job in zip(jobs, all_jobs):
        assert job == received_job

    skip = 2
    limit = 5
    all_jobs = await job_query.get_all_jobs(sa_session, skip=skip, limit=limit)
    assert all_jobs
    assert len(all_jobs) == limit
    for job, received_job in zip(jobs[skip: skip + limit], all_jobs):
        assert job == received_job


@pytest.mark.asyncio
async def test_get_job_by_id(sa_session):
    some_user = UserFactory.build()
    sa_session.add(some_user)
    sa_session.flush()

    n_jobs = 10
    jobs = []
    ids = []
    for _ in range(n_jobs):
        job = JobFactory.build()
        job.user_id = some_user.id
        jobs.append(job)
        ids.append(job.id)
        sa_session.add(job)
    sa_session.flush()

    for i in ids:
        job = await job_query.get_job_by_id(sa_session, i)
        assert job
        assert job.id == i


@pytest.mark.asyncio
async def test_get_job_by_id_not_exists(sa_session):
    job = await job_query.get_job_by_id(sa_session, 42)
    assert job is None


@pytest.mark.asyncio
async def test_delete_job(sa_session, current_user):
    n_jobs = 10
    jobs = []
    for _ in range(n_jobs):
        job = JobFactory.build()
        job.user_id = current_user.id
        jobs.append(job)
        sa_session.add(job)
    sa_session.flush()

    for job in jobs:
        job = await job_query.delete_job(sa_session, job)
        assert job
