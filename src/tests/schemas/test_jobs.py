import pytest

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
