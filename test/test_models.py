import pytest
from httpx import AsyncClient

from ..main import app

@pytest.fixture
async def Client():
    async with AsyncClient(app=app, base_url='http://127.0.0.1:8000') as client:
        yield client

@pytest.mark.asyncio
async def test_create_fleet(Client):
    response = await Client.post(
        "/fleets/",
        json={
            "name": "Test Fleet",
            "description": "Test fleet creation",
        },
    )
    assert response.status_code == 200, response.text