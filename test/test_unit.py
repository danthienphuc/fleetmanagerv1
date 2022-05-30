
from typing import AsyncGenerator
from asyncio import current_task
from ..src.controller import *
from ..src.schemas import *
from ..src.models import *
from ..src import settings
import pytest
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine,AsyncSession,async_scoped_session

@pytest.fixture()
async def test_session() -> AsyncGenerator[AsyncSession, None]:
    engine = create_async_engine(settings.db_url,
            echo=settings.db_echo,
            # pool_size=20, max_overflow=0
        )
    # async with engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.drop_all)
    #     await conn.run_sync(Base.metadata.create_all)

    # expire_on_commit=False will prevent attributes from being expired
    # after commit.
    session_maker = sessionmaker(
        bind=engine, expire_on_commit=False, class_=AsyncSession
    )
    Session = async_scoped_session(session_maker , scopefunc=current_task)
    async with Session() as session:
        yield session
        

@pytest.mark.parametrize("name,description,result",[
    ("Test Fleet 1", "Test Fleet Description 1","Created Successfully"),
    (None, "Test Fleet Description 2",),
    ("Test Fleet 3", None),
    (None, None)
])
@pytest.mark.asyncio
async def test_create_fleet(name:str,description:str,test_session):
    fleet = FleetCreate(name = name, description=description)
    result = await create_obj(Fleet,test_session,**fleet.dict())
    assert result == "Created Successfully"

@pytest.mark.parametrize("name,description,fleet_id", [
    ("Test Vehicle 1", "Test Vehicle Description 1", "1"),
    ("Test Vehicle 2", "Test Vehicle Description 2", "2"),
    ("Test Vehicle 3", "Test Vehicle Description 3", "3")])
@pytest.mark.asyncio
async def test_create_vehicle(name, description, fleet_id, test_session):
    vehicle = VehicleCreate(name= name, description=description,fleet_id = fleet_id)
    result = await create_obj(Vehicle,test_session,**vehicle.dict())
    assert result == "Created Successfully"

@pytest.mark.parametrize("name,age", [
    ("Test Driver 1", "1988-05-13"),
    ("Test Driver 2", "1984-03-09"),
    ("Test Driver 3", "1987-06-09")])
@pytest.mark.asyncio
async def test_create_driver(name, age, test_session):
    driver = DriverCreate(name=name, age=age)
    result = await create_obj(Driver,test_session,**driver.dict())
    assert result == "Created Successfully"

@pytest.mark.parametrize("name,description", [
    ("Test Route 1", "Test Route Description 1"),
    ("Test Route 2", "Test Route Description 2"),
    ("Test Route 3", "Test Route Description 3")])
@pytest.mark.asyncio
async def test_create_route(name,description, test_session):
    route = RouteCreate(name=name, description=description)
    result = await create_obj(Route,test_session,**route.dict())
    assert result == "Created Successfully"

@pytest.mark.parametrize("route_id,driver_id,vehicle_id,start_time,end_time,start_location,end_location,ticket_price", [
    ("1", "1", "1", "2020-01-01T00:00:00Z", "2020-01-01T00:00:00Z", "Test Start Location 1", "Test End Location 1", "10.00"),
    ("2", "2", "2", "2020-01-01T00:00:00Z", "2020-01-01T00:00:00Z", "Test Start Location 2", "Test End Location 2", "20.00"),
    ("3", "3", "3", "2020-01-01T00:00:00Z", "2020-01-01T00:00:00Z", "Test Start Location 3", "Test End Location 3", "30.00"),
    ("1", "2", "2", "2020-01-01T00:00:00Z", "2020-01-01T00:00:00Z", "Test Start Location 4", "Test End Location 4", "40.00"),
    ("2", "3", "3", "2020-01-01T00:00:00Z", "2020-01-01T00:00:00Z", "Test Start Location 5", "Test End Location 5", "50.00"),
    ("3", "1", "1", "2020-01-01T00:00:00Z", "2020-01-01T00:00:00Z", "Test Start Location 6", "Test End Location 6", "60.00"),
    ("1", "3", "3", "2020-01-01T00:00:00Z", "2020-01-01T00:00:00Z", "Test Start Location 7", "Test End Location 7", "70.00"),
    ("2", "1", "1", "2020-01-01T00:00:00Z", "2020-01-01T00:00:00Z", "Test Start Location 8", "Test End Location 8", "80.00"),
    ("3", "2", "2", "2020-01-01T00:00:00Z", "2020-01-01T00:00:00Z", "Test Start Location 9", "Test End Location 9", "90.00")])
@pytest.mark.asyncio
async def test_create_route_details(route_id,driver_id,vehicle_id,start_time,end_time,start_location,end_location,ticket_price,test_session):
    route_detail = RouteDetailCreate(route_id=route_id,driver_id = driver_id, vehicle_id = vehicle_id, start_time = start_time, end_time = end_time, start_location = start_location,end_location= end_location, ticket_price = ticket_price)
    result = await create_obj(RouteDetail,test_session, **route_detail.dict())
    assert result == "Created Successfully"
    


'''

@pytest.mark.parametrize("a,b,expected", [
    (1, 1, 2),
    (1, 2, 3),
    (2, 2, 4),
    (2, 3, 5)])
@pytest.mark.asyncio
async def test_add(Client,a,b,expected):
    response = await Client.get("/")
    assert response.json() == "Connect successfully"

# Fleet tests
################################################################################
@pytest.mark.parametrize("name,description", [
    ("Test Fleet 1", "Test Fleet Description 1"),
    ("Test Fleet 2", "Test Fleet Description 2"),
    ("Test Fleet 3", "Test Fleet Description 3")])
@pytest.mark.asyncio
async def test_create_fleet(Client, name, description):
    response = await Client.post(
        "/fleets/",
        json={
            'name': 'Test Fleet 1',
            'description': 'Test Fleet Description 1',
        }
    )
    assert response.status_code == 200, response.text
    assert response.json() == "Created Successfully" 

@pytest.mark.parametrize("id,name,description", [
    ("1", "Test Fleet 1", "Test Fleet Description 1"),
    ("2", "Test Fleet 2", "Test Fleet Description 2"),
    ("3", "Test Fleet 3", "Test Fleet Description 3")])
@pytest.mark.asyncio
async def test_get_fleet(Client, id, name, description):
    response = await Client.get("/fleets/" + id)
    assert response.status_code == 200, response.text
    assert response.json()["name"] == name
    assert response.json()["description"] == description

@pytest.mark.asyncio
async def test_get_fleets(Client):
    response = await Client.get("/fleets/")
    assert response.status_code == 200, response.text
    assert len(response.json()) == 3
    for i in range(3):
        assert response.json()[i]["id"] == str(i + 1)
        assert response.json()[i]["name"] == "Test Fleet " + str(i + 1)
        assert response.json()[i]["description"] == "Test Fleet Description " + str(i + 1)


@pytest.mark.parametrize("id,name,description", [
    ("1", "Test Fleet 1", "Test Fleet Description 1 Updated"),
    ("2", "Test Fleet 2", "Test Fleet Description 2 Updated"),
    ("3", "Test Fleet 3", "Test Fleet Description 3 Updated")])

@pytest.mark.asyncio
async def test_update_fleet(Client ,id, name, description):
    response = await Client.put(
        "/fleets/" + id,
        json={
            "name": name,
            "description": description,
        },
    )
    assert response.status_code == 200, response.text
    assert response.json()["detail"] == "Updated successfully"


# Vehicle tests
################################################################################



@pytest.mark.parametrize("id,name,description,fleet_id", [
    ("1", "Test Vehicle 1", "Test Vehicle Description 1", "1"),
    ("2", "Test Vehicle 2", "Test Vehicle Description 2", "2"),
    ("3", "Test Vehicle 3", "Test Vehicle Description 3", "1")])
@pytest.mark.asyncio
async def test_get_vehicle(Client, id, name, description, fleet_id):
    response = await Client.get("/vehicles/" + id)
    assert response.status_code == 200, response.text
    assert response.json()["id"] == id
    assert response.json()["name"] == name
    assert response.json()["description"] == description
    assert response.json()["fleet_id"] == fleet_id


@pytest.mark.asyncio
async def test_get_vehicles(Client):
    response = await Client.get("/vehicles/")
    assert response.status_code == 200, response.text
    assert len(response.json()) == 3
    for i in range(3):
        assert response.json()[i]["id"] == str(i + 1)
        assert response.json()[i]["name"] == "Test Vehicle " + str(i + 1)
        assert response.json()[i]["description"] == "Test Vehicle Description " + str(i + 1)
        assert response.json()[i]["fleet_id"] == ((i+1)%2)*(-1)+2

@pytest.mark.parametrize("id,name,description,fleet_id", [
    ("1", "Test Vehicle 1", "Test Vehicle Description 1 Updated", "1"),
    ("2", "Test Vehicle 2", "Test Vehicle Description 2 Updated", "2"),
    ("3", "Test Vehicle 3", "Test Vehicle Description 3 Updated", "1")])
@pytest.mark.asyncio
async def test_update_vehicle(Client, id, name, description, fleet_id):
    response = await Client.put(
        "/vehicles/"+id,
        json={
            "name": name,
            "description": description,
            "fleet_id": fleet_id,
        },
    )
    assert response.status_code == 200, response.text
    assert response.json()["detail"] == "Updated successfully"


# Driver tests
################################################################################

@pytest.mark.parametrize("name,description,age", [
    ("Test Driver 1", "Test Driver Description 1", "1988-05-13"),
    ("Test Driver 2", "Test Driver Description 2", "1984-03-09"),
    ("Test Driver 3", "Test Driver Description 3", "1987-06-09")])
@pytest.mark.asyncio
async def test_create_driver(Client, name, description, age):
    response = await Client.post(
        "/drivers/",
        json={
            "name": name,
            "description": description,
            "age": age,
        },
    )
    assert response.status_code == 200, response.text
    assert response.json()["detail"] == "Created Successfully"

@pytest.mark.parametrize("id,name,description,age", [
    ("1", "Test Driver 1", "Test Driver Description 1", "1988-05-13"),
    ("2", "Test Driver 2", "Test Driver Description 2", "1984-03-09"),
    ("3", "Test Driver 3", "Test Driver Description 3", "1987-06-09")])
@pytest.mark.asyncio
async def test_get_driver(Client, id, name, description, age):
    response = await Client.get("/drivers/" + id)
    assert response.status_code == 200, response.text
    assert response.json()["id"] == id
    assert response.json()["name"] == name
    assert response.json()["description"] == description
    assert response.json()["age"] == age

@pytest.mark.asyncio
async def test_get_drivers(Client):
    response = await Client.get("/drivers/")
    assert response.status_code == 200, response.text
    assert len(response.json()) == 3
    for i in range(3):
        assert response.json()[i]["id"] == str(i + 1)
        assert response.json()[i]["name"] == "Test Driver " + str(i + 1)
        assert response.json()[i]["description"] == "Test Driver Description " + str(i + 1)
        assert response.json()[i]["age"] in ["1988-05-13", "1984-03-09", "1987-06-09"]

@pytest.mark.parametrize("id,name,description,age", [
    ("1", "Test Driver 1", "Test Driver Description 1 Updated", "1988-05-13"),
    ("2", "Test Driver 2", "Test Driver Description 2 Updated", "1984-03-09"),
    ("3", "Test Driver 3", "Test Driver Description 3 Updated", "1987-06-09")])
@pytest.mark.asyncio
async def test_update_driver(Client, id, name, description, age):
    response = await Client.put(
        "/drivers/" + id,
        json={
            "name": name,
            "description": description,
            "age": age,
        },
    )
    assert response.status_code == 200, response.text
    assert response.json()["detail"] == "Updated Successfully"

# Route tests
################################################################################

@pytest.mark.parametrize("name,description", [
    ("Test Route 1", "Test Route Description 1"),
    ("Test Route 2", "Test Route Description 2"),
    ("Test Route 3", "Test Route Description 3")])
@pytest.mark.asyncio
async def test_create_route(Client, name, description):
    response = await Client.post(
        "/routes/",
        json={
            "name": name,
            "description": description,
        },
    )
    assert response.status_code == 200, response.text
    assert response.json()["detail"] == "Created Successfully"

@pytest.mark.parametrize("id,name,description", [
    ("1", "Test Route 1", "Test Route Description 1"),
    ("2", "Test Route 2", "Test Route Description 2"),
    ("3", "Test Route 3", "Test Route Description 3")])
@pytest.mark.asyncio
async def test_get_route(Client, id, name, description):
    response = await Client.get("/routes/" + id)
    assert response.status_code == 200, response.text
    assert response.json()["id"] == id
    assert response.json()["name"] == name
    assert response.json()["description"] == description

@pytest.mark.asyncio
async def test_get_routes(Client):
    response = await Client.get("/routes/")
    assert response.status_code == 200, response.text
    assert len(response.json()) == 3
    for i in range(3):
        assert response.json()[i]["id"] == str(i + 1)
        assert response.json()[i]["name"] == "Test Route " + str(i + 1)
        assert response.json()[i]["description"] == "Test Route Description " + str(i + 1)

@pytest.mark.parametrize("id,name,description", [
    ("1", "Test Route 1", "Test Route Description 1 Updated"),
    ("2", "Test Route 2", "Test Route Description 2 Updated"),
    ("3", "Test Route 3", "Test Route Description 3 Updated")])
@pytest.mark.asyncio
async def test_update_route(Client, id, name, description):
    response = await Client.put(
        "/routes/"+id,
        json={
            "name": name,
            "description": description,
        },
    )
    assert response.status_code == 200, response.text
    assert response.json()["detail"] == "Updated Successfully"

# Route Details tests
################################################################################

@pytest.mark.parametrize("route_id,driver_id,vehicle_id,start_time,end_time,start_location,end_location,ticket_price", [
    ("1", "1", "1", "2020-01-01T00:00:00Z", "2020-01-01T00:00:00Z", "Test Start Location 1", "Test End Location 1", "10.00"),
    ("2", "2", "2", "2020-01-01T00:00:00Z", "2020-01-01T00:00:00Z", "Test Start Location 2", "Test End Location 2", "20.00"),
    ("3", "3", "3", "2020-01-01T00:00:00Z", "2020-01-01T00:00:00Z", "Test Start Location 3", "Test End Location 3", "30.00"),
    ("1", "2", "2", "2020-01-01T00:00:00Z", "2020-01-01T00:00:00Z", "Test Start Location 4", "Test End Location 4", "40.00"),
    ("2", "3", "3", "2020-01-01T00:00:00Z", "2020-01-01T00:00:00Z", "Test Start Location 5", "Test End Location 5", "50.00"),
    ("3", "1", "1", "2020-01-01T00:00:00Z", "2020-01-01T00:00:00Z", "Test Start Location 6", "Test End Location 6", "60.00"),
    ("1", "3", "3", "2020-01-01T00:00:00Z", "2020-01-01T00:00:00Z", "Test Start Location 7", "Test End Location 7", "70.00"),
    ("2", "1", "1", "2020-01-01T00:00:00Z", "2020-01-01T00:00:00Z", "Test Start Location 8", "Test End Location 8", "80.00"),
    ("3", "2", "2", "2020-01-01T00:00:00Z", "2020-01-01T00:00:00Z", "Test Start Location 9", "Test End Location 9", "90.00")])
@pytest.mark.asyncio
async def test_create_route_details(Client, route_id, vehicle_id,  driver_id,start_time, end_time, start_location, end_location, ticket_price):
    response = await Client.post(
        "/routes/1/details/",
        json={
            "route_id": route_id,
            "vehicle_id": vehicle_id,
            "driver_id": driver_id,
            "start_time": start_time,
            "end_time": end_time,
            "start_location": start_location,
            "end_location": end_location,
            "ticket_price": ticket_price
        },
    )
    assert response.status_code == 200, response.text
    assert response.json()["detail"] == "Created Successfully"

@pytest.mark.asyncio
async def test_get_route_details_list(Client):
    response = await Client.get("/routes/1/details/")
    assert response.status_code == 200, response.text
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "Test Route Detail"
    assert response.json()[0]["description"] == "Test route detail creation"

@pytest.mark.parametrize("route_id,vehicle_id,driver_id,start_time,end_time,start_location,end_location,ticket_price", [
    ("1", "1", "1", "2020-01-01T00:00:00Z", "2020-01-01T00:00:00Z", "Test Start Location 1 Updated", "Test End Location Updated", "10.00"),
    ("2", "2", "2", "2020-01-01T00:00:00Z", "2020-01-01T00:00:00Z", "Test Start Location 2 Updated", "Test End Location Updated", "20.00"),
    ("3", "3", "3", "2020-01-01T00:00:00Z", "2020-01-01T00:00:00Z", "Test Start Location 3 Updated", "Test End Location Updated", "30.00"),
    ("1", "2", "2", "2020-01-01T00:00:00Z", "2020-01-01T00:00:00Z", "Test Start Location 4 Updated", "Test End Location Updated", "40.00"),
    ("2", "3", "3", "2020-01-01T00:00:00Z", "2020-01-01T00:00:00Z", "Test Start Location 5 Updated", "Test End Location Updated", "50.00"),
    ("3", "1", "1", "2020-01-01T00:00:00Z", "2020-01-01T00:00:00Z", "Test Start Location 6 Updated", "Test End Location Updated", "60.00"),
    ("1", "3", "3", "2020-01-01T00:00:00Z", "2020-01-01T00:00:00Z", "Test Start Location 7 Updated", "Test End Location Updated", "70.00"),
    ("2", "1", "1", "2020-01-01T00:00:00Z", "2020-01-01T00:00:00Z", "Test Start Location 8 Updated", "Test End Location Updated", "80.00"),
    ("3", "2", "2", "2020-01-01T00:00:00Z", "2020-01-01T00:00:00Z", "Test Start Location 9 Updated", "Test End Location Updated", "90.00")])
@pytest.mark.asyncio
async def test_update_route_details(Client, route_id, vehicle_id,  driver_id,start_time, end_time, start_location, end_location, ticket_price):
    response = await Client.put(
        "/routedetails/1",
        json={
            "name": "Test Route Detail",
            "description": "Test route detail update"
        },
    )
    assert response.status_code == 200, response.text
    assert response.json()["detail"] == "Updated Successfully"




# Delete tests
################################################################################

@pytest.mark.parametrize("route_id,vehicle_id", [
    ("1", "1"),
    ("2", "2"),
    ("3", "3"),
    ("1", "2"),
    ("2", "3"),
    ("3", "1"),
    ("1", "3"),
    ("2", "1"),
    ("3", "2")])

@pytest.mark.asyncio
async def test_delete_route_details(Client, route_id, vehicle_id):
    response = await Client.delete("/routedetails/"+route_id+"/"+vehicle_id)
    assert response.status_code == 204, response.text

@pytest.mark.parametrize("id", ["1", "2", "3"])
@pytest.mark.asyncio
async def test_delete_route(Client, id):
    response = await Client.delete("/routes/"+id)
    assert response.status_code == 204, response.text
    assert response.json()["detail"] == "Deleted successfully"

@pytest.mark.parametrize("id", ["1", "2", "3"])
@pytest.mark.asyncio
async def test_delete_driver(Client, id):
    response = await Client.delete("/drivers/"+id)
    assert response.status_code == 204, response.text
    assert response.json()["detail"] == "Deleted successfully"

@pytest.mark.parametrize("id", ["1", "2", "3"])
@pytest.mark.asyncio
async def test_delete_vehicle(Client, id):
    response = await Client.delete("/vehicles/"+id)
    assert response.status_code == 204, response.text
    assert response.json()["detail"] == "Deleted successfully"

@pytest.mark.parametrize("id", ["1", "2", "3"])
@pytest.mark.asyncio
async def test_delete_fleet(Client, id):
    response = await Client.delete("/fleets/" + id)
    assert response.status_code == 204, response.text
    assert response.json()["detail"] == "Deleted successfully"


'''