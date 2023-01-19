import pytest
from queries import response as response_query
from fixtures.responses import ResponseFactory
from fixtures.jobs import JobFactory
from fixtures.users import UserFactory
from schemas import ResponseInSchema


@pytest.mark.asyncio
async def test_response_job(sa_session, current_user):
    some_user = UserFactory.build()
    sa_session.add(some_user)
    sa_session.flush()

    some_job = JobFactory.build()
    some_job.user_id = some_user.id
    sa_session.add(some_job)
    sa_session.flush()

    response = ResponseInSchema(
        job_id=some_job.id,
        message='hello there, i want to work on your work!'
    )
    response = await response_query.response_job(sa_session, response, current_user)

    assert response
    assert response.job_id == some_job.id
    assert response.user_id == current_user.id


@pytest.mark.asyncio
async def test_get_response_by_user_id(sa_session):
    some_user = UserFactory.build()
    sa_session.add(some_user)
    sa_session.flush()

    some_job = JobFactory.build()
    some_job.user_id = some_user.id
    sa_session.add(some_job)
    sa_session.flush()

    another_job = JobFactory.build()
    another_job.user_id = some_user.id
    sa_session.add(another_job)
    sa_session.flush()

    n_some_responses = 1
    n_another_responses = 3
    for _ in range(n_some_responses):
        response = ResponseFactory.build()
        response.user_id = some_user.id
        response.job_id = some_job.id
        sa_session.add(response)
    for _ in range(n_another_responses):
        response = ResponseFactory.build()
        response.user_id = some_user.id
        response.job_id = another_job.id
        sa_session.add(response)

    some_responses = await response_query.get_response_by_user_id(sa_session, some_job.id)
    assert some_responses
    assert len(some_responses) == n_some_responses

    another_responses = await response_query.get_response_by_user_id(sa_session, another_job.id)
    assert another_responses
    assert len(another_responses) == n_another_responses
