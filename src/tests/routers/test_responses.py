import pytest

from fixtures.users import UserFactory
from fixtures.jobs import JobFactory
from fixtures.responses import ResponseFactory
from schemas import ResponseInSchema
from fastapi import status


@pytest.mark.asyncio
async def test_get_response_by_user_id(sa_session, client_app):
    some_user = UserFactory.build()
    sa_session.add(some_user)
    sa_session.flush()

    some_job = JobFactory.build()
    some_job.user_id = some_user.id
    sa_session.add(some_job)
    sa_session.flush()

    responses = []
    n_responses = 10
    for _ in range(n_responses):
        response = ResponseFactory.build()
        response.user_id = some_user.id
        response.job_id = some_job.id

        sa_session.add(response)
        responses.append(response)
    sa_session.flush()

    all_responses = await client_app.get(url=f'/responses?job_id={some_job.id}')

    assert len(all_responses.json()) == n_responses
    for i in range(n_responses):
        assert all_responses.json()[i]['message'] == responses[i].message


@pytest.mark.asyncio
async def test_response_job_as_not_company(sa_session, client_app, current_user):
    current_user.is_company = False
    sa_session.add(current_user)
    sa_session.flush()

    some_user = UserFactory.build()
    sa_session.add(some_user)
    sa_session.flush()

    some_job = JobFactory.build()
    some_job.user_id = some_user.id
    sa_session.add(some_job)
    sa_session.flush()

    response = ResponseFactory.build()
    response_create = ResponseInSchema(
        job_id=some_job.id,
        message=response.message
    )

    created_response = await client_app.post(
        url=f'/responses?job_id={some_job.id}',
        json=response_create.dict()
    )

    assert created_response.json()['message'] == response.message


@pytest.mark.asyncio
async def test_response_job_as_company(sa_session, client_app, current_user):
    current_user.is_company = True
    sa_session.add(current_user)
    sa_session.flush()

    some_user = UserFactory.build()
    sa_session.add(some_user)
    sa_session.flush()

    some_job = JobFactory.build()
    some_job.user_id = some_user.id
    sa_session.add(some_job)
    sa_session.flush()

    response = ResponseFactory.build()
    response_create = ResponseInSchema(
        job_id=some_job.id,
        message=response.message
    )

    created_response = await client_app.post(
        url=f'/responses?job_id={some_job.id}',
        json=response_create.dict()
    )

    assert created_response.status_code == status.HTTP_403_FORBIDDEN
