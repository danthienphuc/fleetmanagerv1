from typing import Dict, Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from ..src.main import app
from ..src.old.database import async_db_session

@pytest.fixture(scope="session")
def db() -> Generator:
    yield async_db_session()

@pytest.fixture(scope="module")
def Client() -> Generator:
    with TestClient(app) as c:
        yield c
        
@pytest.mark.parametrize("a,b,expected", [
    (1, 1, 2),
    (1, 2, 3),
    (2, 2, 4),
    (2, 3, 5)])
@pytest.mark.asyncio
def test_add(Client,a,b,expected):
    response = Client.get("/")
    assert response.json() == "Connect successfully"

@pytest.mark.parametrize("name,description", [
    ("Test Fleet 1", "Test Fleet Description 1"),
    ("Test Fleet 2", "Test Fleet Description 2"),
    ("Test Fleet 3", "Test Fleet Description 3")])
@pytest.mark.asyncio
def test_create_fleet(Client, name, description):
    response = Client.post(
        "/fleets/",
        json={
            'name': 'Test Fleet 1',
            'description': 'Test Fleet Description 1',
        }
    )
    assert response.status_code == 200, response.text
    assert response.json() == "Created Successfully" 