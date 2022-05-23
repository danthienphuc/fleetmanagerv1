import pytest
from httpx import AsyncClient

from ..main import app

@pytest.fixture
async def Client():
    async with AsyncClient(app=app, base_url='http://127.0.0.1:8000') as client:
        yield client


# Fleet tests
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
    assert response.json()["name"] == "Test Fleet"

@pytest.mark.asyncio
async def test_get_fleet(Client):
    response = await Client.get("/fleets/1")
    assert response.status_code == 200, response.text
    assert response.json()["name"] == "Test Fleet"
    assert response.json()["description"] == "Test fleet creation"

@pytest.mark.asyncio
async def test_get_fleets(Client):
    response = await Client.get("/fleets/")
    assert response.status_code == 200, response.text
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "Test Fleet"
    assert response.json()[0]["description"] == "Test fleet creation"

@pytest.mark.asyncio
async def test_update_fleet(Client):
    response = await Client.put(
        "/fleets/1",
        json={
            "name": "Test Fleet",
            "description": "Test fleet update",
        },
    )
    assert response.status_code == 200, response.text
    assert response.json()["name"] == "Test Fleet"
    assert response.json()["description"] == "Test fleet update"

@pytest.mark.asyncio
async def test_delete_fleet(Client):
    response = await Client.delete("/fleets/1")
    assert response.status_code == 204, response.text


# Vehicle tests
@pytest.mark.asyncio
async def test_create_vehicle(Client):
    response = await Client.post(
        "/vehicles/",
        json={
            "name": "Test Vehicle",
            "description": "Test vehicle creation",
            "fleet": 1,
        },
    )
    assert response.status_code == 200, response.text
    assert response.json()["name"] == "Test Vehicle"
    assert response.json()["description"] == "Test vehicle creation"
    assert response.json()["fleet"] == 1

@pytest.mark.asyncio
async def test_get_vehicle(Client):
    response = await Client.get("/vehicles/1")
    assert response.status_code == 200, response.text
    assert response.json()["name"] == "Test Vehicle"
    assert response.json()["description"] == "Test vehicle creation"
    assert response.json()["fleet"] == 1

@pytest.mark.asyncio
async def test_get_vehicles(Client):
    response = await Client.get("/vehicles/")
    assert response.status_code == 200, response.text
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "Test Vehicle"
    assert response.json()[0]["description"] == "Test vehicle creation"
    assert response.json()[0]["fleet"] == 1

@pytest.mark.asyncio
async def test_update_vehicle(Client):
    response = await Client.put(
        "/vehicles/1",
        json={
            "name": "Test Vehicle",
            "description": "Test vehicle update",
            "fleet": 1,
        },
    )
    assert response.status_code == 200, response.text
    assert response.json()["name"] == "Test Vehicle"
    assert response.json()["description"] == "Test vehicle update"
    assert response.json()["fleet"] == 1

@pytest.mark.asyncio
async def test_delete_vehicle(Client):
    response = await Client.delete("/vehicles/1")
    assert response.status_code == 204, response.text


# Driver tests
@pytest.mark.asyncio
async def test_create_driver(Client):
    response = await Client.post(
        "/drivers/",
        json={
            "name": "Test Driver",
            "description": "Test driver creation",
            "age": "1988-08-25",
        },
    )
    assert response.status_code == 200, response.text
    assert response.json()["name"] == "Test Driver"
    assert response.json()["description"] == "Test driver creation"
    assert response.json()["age"] == "1988-08-25"

@pytest.mark.asyncio
async def test_get_driver(Client):
    response = await Client.get("/drivers/1")
    assert response.status_code == 200, response.text
    assert response.json()["name"] == "Test Driver"
    assert response.json()["description"] == "Test driver creation"
    assert response.json()["age"] == "1988-08-25"

@pytest.mark.asyncio
async def test_get_drivers(Client):
    response = await Client.get("/drivers/")
    assert response.status_code == 200, response.text
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "Test Driver"
    assert response.json()[0]["description"] == "Test driver creation"
    assert response.json()[0]["age"] == "1988-08-25"

@pytest.mark.asyncio
async def test_update_driver(Client):
    response = await Client.put(
        "/drivers/1",
        json={
            "name": "Test Driver",
            "description": "Test driver update",
            "age": "1988-08-25",
        },
    )
    assert response.status_code == 200, response.text
    assert response.json()["name"] == "Test Driver"
    assert response.json()["description"] == "Test driver update"
    assert response.json()["age"] == "1988-08-25"

@pytest.mark.asyncio
async def test_delete_driver(Client):
    response = await Client.delete("/drivers/1")
    assert response.status_code == 204, response.text

# Route tests
@pytest.mark.asyncio
async def test_create_route(Client):
    response = await Client.post(
        "/routes/",
        json={
            "name": "Test Route",
            "description": "Test route creation"
        },
    )
    assert response.status_code == 200, response.text
    assert response.json()["name"] == "Test Route"
    assert response.json()["description"] == "Test route creation"

@pytest.mark.asyncio
async def test_get_route(Client):
    response = await Client.get("/routes/1")
    assert response.status_code == 200, response.text
    assert response.json()["name"] == "Test Route"
    assert response.json()["description"] == "Test route creation"

@pytest.mark.asyncio
async def test_get_routes(Client):
    response = await Client.get("/routes/")
    assert response.status_code == 200, response.text
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "Test Route"
    assert response.json()[0]["description"] == "Test route creation"

@pytest.mark.asyncio
async def test_update_route(Client):
    response = await Client.put(
        "/routes/1",
        json={
            "name": "Test Route",
            "description": "Test route update"
        },
    )
    assert response.status_code == 200, response.text
    assert response.json()["name"] == "Test Route"
    assert response.json()["description"] == "Test route update"

@pytest.mark.asyncio
async def test_delete_route(Client):
    response = await Client.delete("/routes/1")
    assert response.status_code == 204, response.text

# Route Details tests

@pytest.mark.asyncio
async def test_create_route_details(Client):
    response = await Client.post(
        "/routes/1/details/",
        json={
            "name": "Test Route Detail",
            "description": "Test route detail creation"
        },
    )
    assert response.status_code == 200, response.text
    assert response.json()["name"] == "Test Route Detail"
    assert response.json()["description"] == "Test route detail creation"

@pytest.mark.asyncio
async def test_get_route_details(Client):
    response = await Client.get("/routedetails/1")
    assert response.status_code == 200, response.text
    assert response.json()["name"] == "Test Route Detail"
    assert response.json()["description"] == "Test route detail creation"

@pytest.mark.asyncio
async def test_get_route_details_list(Client):
    response = await Client.get("/routes/1/details/")
    assert response.status_code == 200, response.text
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "Test Route Detail"
    assert response.json()[0]["description"] == "Test route detail creation"

@pytest.mark.asyncio
async def test_update_route_details(Client):
    response = await Client.put(
        "/routedetails/1",
        json={
            "name": "Test Route Detail",
            "description": "Test route detail update"
        },
    )
    assert response.status_code == 200, response.text
    assert response.json()["name"] == "Test Route Detail"
    assert response.json()["description"] == "Test route detail update"

@pytest.mark.asyncio
async def test_delete_route_details(Client):
    response = await Client.delete("/routedetails/1")
    assert response.status_code == 204, response.text



