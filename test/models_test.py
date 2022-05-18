from email.mime import base
import re
from urllib import response
from models import Fleet
import pytest
from httpx import AsyncClient

from ..main import app

base_url = 'http://localhost:8080/'


@pytest.mark.anyio
async def test_root():
    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Tomato"}
    
# Fleet CRUD methods test 
fleet_url = base_url + '/fleet/'

# Create fleet methods
async def test_create_fleet():
    async with AsyncClient(app=app, base_url=fleet_url) as ac:
        response = await ac.post("/")
    assert response.status_code == 201
    assert response.json() == {"message":"Create Successful"}
    
# Get a fleet method
async def test_get_fleet():
    async with AsyncClient(app=app, base_url=fleet_url) as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert response.json() == {"message

    

    

