
from datetime import date, datetime
from os import name
from re import I
from typing import AsyncGenerator
from asyncio import current_task
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine,AsyncSession,async_scoped_session
import pytest
from ..src.controller import *
from ..src.schemas import *
from ..src.models import *
from ..src import settings


@pytest.fixture()
def test_engine():
    engine = create_async_engine(settings.db_url,
            echo=settings.db_echo,
            # pool_size=20, max_overflow=0
        )
    yield engine

@pytest.fixture()
async def test_session(test_engine) -> AsyncGenerator[AsyncSession, None]:
    

    # expire_on_commit=False will prevent attributes from being expired
    # after commit.
    session_maker = sessionmaker(
        bind=test_engine, expire_on_commit=False, class_=AsyncSession
    )
    Session = async_scoped_session(session_maker , scopefunc=current_task)
    async with Session() as session:
        yield session
        
@pytest.mark.asyncio
async def test_refresh_db(test_engine):
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


def string_to_date(string):
    string = string.split("-")
    return date(int(string[0]),int(string[1]),int(string[2]))

# Test Create

# Test Create Fleet
@pytest.mark.parametrize("name,description,id",[
    ("Test Fleet 1", "Test Fleet Description 1",1),
    ("Test Fleet 2", "Test Fleet Description 2",2),
    ("Test Fleet 3", "Test Fleet Description 3",3)
])
@pytest.mark.asyncio
async def test_create_fleet(name:str,description:str,id:int,test_session):
    fleet = FleetCreate(name = name, description=description)
    response = await create_obj(Fleet,test_session,**fleet.dict())
    assert response.id == id
    assert response.name == name
    assert response.description == description

# Test Create Vehicle
@pytest.mark.parametrize("name,description,fleet_id,id", [
    ("Test Vehicle 1", "Test Vehicle Description 1", 1,1),
    ("Test Vehicle 2", "Test Vehicle Description 2", 2,2),
    ("Test Vehicle 3", "Test Vehicle Description 3", 3,3)])
@pytest.mark.asyncio
async def test_create_vehicle(name:str, description:str, fleet_id:int, id:int, test_session):
    vehicle = VehicleCreate(name= name, description=description,fleet_id = fleet_id)
    response = await create_obj(Vehicle,test_session,**vehicle.dict())
    assert response.id == id
    assert response.name == name
    assert response.description == description
    assert response.fleet_id == fleet_id
    
# Test Create Driver
@pytest.mark.parametrize("name,age,id", [
    ("Test Driver 1", '1988-05-13',1),
    ("Test Driver 2", '1984-03-09',2),
    ("Test Driver 3", '1987-06-09',3)])
@pytest.mark.asyncio
async def test_create_driver(name, age,id, test_session):
    driver = DriverCreate(name=name, age=age)
    response = await create_obj(Driver,test_session,**driver.dict())
    assert response.id == id
    assert response.name == name
    assert response.age == string_to_date(age)

# Test Create Route
@pytest.mark.parametrize("name,description,id", [
    ("Test Route 1", "Test Route Description 1",1),
    ("Test Route 2", "Test Route Description 2",2),
    ("Test Route 3", "Test Route Description 3",3)])
@pytest.mark.asyncio
async def test_create_route(name,description,id, test_session):
    route = RouteCreate(name=name, description=description)
    response = await create_obj(Route,test_session,**route.dict())
    assert response.id == id
    assert response.name == name
    assert response.description == description


# Test Create Route Detail
@pytest.mark.parametrize("route_id,driver_id,vehicle_id,start_time,end_time,start_location,end_location,ticket_price", [
    ("1", "1", "1", "2020-01-01T00:00:00Z", "2020-01-01T00:00:00Z", "Test Start Location 1", "Test End Location 1", 10),
    ("2", "2", "2", "2020-01-01T00:00:00Z", "2020-01-01T00:00:00Z", "Test Start Location 2", "Test End Location 2", 20),
    ("3", "3", "3", "2020-01-01T00:00:00Z", "2020-01-01T00:00:00Z", "Test Start Location 3", "Test End Location 3", 30),
    ("1", "2", "2", "2020-01-01T00:00:00Z", "2020-01-01T00:00:00Z", "Test Start Location 4", "Test End Location 4", 40),
    ("2", "3", "3", "2020-01-01T00:00:00Z", "2020-01-01T00:00:00Z", "Test Start Location 5", "Test End Location 5", 50),
    ("3", "1", "1", "2020-01-01T00:00:00Z", "2020-01-01T00:00:00Z", "Test Start Location 6", "Test End Location 6", 60),
    ("1", "3", "3", "2020-01-01T00:00:00Z", "2020-01-01T00:00:00Z", "Test Start Location 7", "Test End Location 7", 70),
    ("2", "1", "1", "2020-01-01T00:00:00Z", "2020-01-01T00:00:00Z", "Test Start Location 8", "Test End Location 8", 80),
    ("3", "2", "2", "2020-01-01T00:00:00Z", "2020-01-01T00:00:00Z", "Test Start Location 9", "Test End Location 9", 90)])
@pytest.mark.asyncio
async def test_create_route_details(route_id,driver_id,vehicle_id\
    ,start_time,end_time,start_location,end_location,ticket_price,test_session):
    route_detail = RouteDetailCreate(route_id=route_id,driver_id = driver_id\
        ,vehicle_id = vehicle_id, start_time = start_time, end_time = end_time\
            ,start_location = start_location,end_location= end_location\
                , ticket_price = ticket_price)
    response = await create_obj(RouteDetail,test_session, **route_detail.dict())
    assert response.route_id == route_id
    assert response.driver_id == driver_id
    assert response.vehicle_id == vehicle_id
    assert response.start_time == datetime.strftime(start_time, '%Y-%m-%dT%H:%M:%SZ')
    assert response.end_time == datetime.strftime(start_time, '%Y-%m-%dT%H:%M:%SZ')
    assert response.start_location == start_location
    assert response.end_location == end_location
    assert response.ticket_price == ticket_price

# Test get all objects

# Test get all fleets
@pytest.mark.asyncio
async def test_get_all_fleets(test_session):
    response = await get_all_obj(Fleet,test_session)
    assert len(response) == 3
    assert response[0].id == 1
    assert response[0].name == "Test Fleet 1"
    assert response[0].description == "Test Fleet Description 1"
    assert response[1].id == 2
    assert response[1].name == "Test Fleet 2"
    assert response[1].description == "Test Fleet Description 2"
    assert response[2].id == 3
    assert response[2].name == "Test Fleet 3"
    assert response[2].description == "Test Fleet Description 3"

# Test get all vehicles
@pytest.mark.asyncio
async def test_get_all_vehicles(test_session):
    response = await get_all_obj(Vehicle,test_session)
    assert len(response) == 3
    assert response[0].id == 1
    assert response[0].name == "Test Vehicle 1"
    assert response[0].description == "Test Vehicle Description 1"
    assert response[0].fleet_id == 1
    assert response[1].id == 2
    assert response[1].name == "Test Vehicle 2"
    assert response[1].description == "Test Vehicle Description 2"
    assert response[1].fleet_id == 2
    assert response[2].id == 3
    assert response[2].name == "Test Vehicle 3"
    assert response[2].description == "Test Vehicle Description 3"
    assert response[2].fleet_id == 3

# Test get all drivers
@pytest.mark.asyncio
async def test_get_all_drivers(test_session):
    response = await get_all_obj(Driver,test_session)
    assert len(response) == 3
    assert response[0].id == 1
    assert response[0].name == "Test Driver 1"
    assert response[0].age == string_to_date("2020-01-01")
    assert response[1].vehicle_id == 2
    assert response[1].name == "Test Driver 2"
    assert response[1].age == string_to_date("2020-01-01")
    assert response[2].vehicle_id == 3
    assert response[2].name == "Test Driver 3"
    assert response[2].age == string_to_date("2020-01-01")

# Test get all routes
@pytest.mark.asyncio
async def test_get_all_routes(test_session):
    response = await get_all_obj(Route,test_session)
    assert len(response) == 3
    assert response[0].id == 1
    assert response[0].name == "Test Route 1"
    assert response[0].description == "Test Route Description 1"
    assert response[1].id == 2
    assert response[1].name == "Test Route 2"
    assert response[1].description == "Test Route Description 2"
    assert response[2].id == 3
    assert response[2].name == "Test Route 3"
    assert response[2].description == "Test Route Description 3"

# Test get all route details
@pytest.mark.asyncio
async def test_get_all_route_details(test_session):
    response = await get_all_obj(RouteDetail,test_session)
    assert len(response) == 9
    assert response[0].route_id == 1
    assert response[0].driver_id == 1
    assert response[0].vehicle_id == 1
    assert response[0].start_time == datetime.strptime("2020-01-01T00:00:00Z","%Y-%m-%dT%H:%M:%SZ")
    assert response[0].end_time == datetime.strptime("2020-01-01T00:00:00Z","%Y-%m-%dT%H:%M:%SZ")
    assert response[0].start_location == "Test Start Location 1"
    assert response[0].end_location == "Test End Location 1"
    assert response[0].ticket_price == 10
    assert response[1].route_id == 2
    assert response[1].driver_id == 2
    assert response[1].vehicle_id == 2
    assert response[1].start_time == datetime.strptime("2020-01-01T00:00:00Z","%Y-%m-%dT%H:%M:%SZ")
    assert response[1].end_time == datetime.strptime("2020-01-01T00:00:00Z","%Y-%m-%dT%H:%M:%SZ")
    assert response[1].start_location == "Test Start Location 2"
    assert response[1].end_location == "Test End Location 2"
    assert response[1].ticket_price == 20
    assert response[2].route_id == 3
    assert response[2].driver_id == 3
    assert response[2].vehicle_id == 3
    assert response[2].start_time == datetime.strptime("2020-01-01T00:00:00Z","%Y-%m-%dT%H:%M:%SZ")
    assert response[2].end_time == datetime.strptime("2020-01-01T00:00:00Z","%Y-%m-%dT%H:%M:%SZ")
    assert response[2].start_location == "Test Start Location 3"
    assert response[2].end_location == "Test End Location 3"
    assert response[2].ticket_price == 30
    assert response[5].route_id == 3
    assert response[5].driver_id == 1
    assert response[5].vehicle_id == 1
    assert response[5].start_time == datetime.strptime("2020-01-01T00:00:00Z","%Y-%m-%dT%H:%M:%SZ")
    assert response[5].end_time == datetime.strptime("2020-01-01T00:00:00Z","%Y-%m-%dT%H:%M:%SZ")
    assert response[5].start_location == "Test Start Location 6"
    assert response[5].end_location == "Test End Location 6"
    assert response[5].ticket_price == 60
    assert response[6].route_id == 1
    assert response[6].driver_id == 3
    assert response[6].vehicle_id == 3
    assert response[6].start_time == datetime.strptime("2020-01-01T00:00:00Z","%Y-%m-%dT%H:%M:%SZ")
    assert response[6].end_time == datetime.strptime("2020-01-01T00:00:00Z","%Y-%m-%dT%H:%M:%SZ")
    assert response[6].start_location == "Test Start Location 7"
    assert response[6].end_location == "Test End Location 7"
    assert response[6].ticket_price == 70
    assert response[8].route_id == 3
    assert response[8].driver_id == 2
    assert response[8].vehicle_id == 2
    assert response[8].start_time == datetime.strptime("2020-01-01T00:00:00Z","%Y-%m-%dT%H:%M:%SZ")
    assert response[8].end_time == datetime.strptime("2020-01-01T00:00:00Z","%Y-%m-%dT%H:%M:%SZ")
    assert response[8].start_location == "Test Start Location 9"
    assert response[8].end_location == "Test End Location 9"
    assert response[8].ticket_price == 90

# Test get an object by id

# Test get an fleet
@pytest.mark.parametrize("id, name, description",
[(1,"Test Fleet 1","Test Fleet Description 1"),
(2,"Test Fleet 2","Test Fleet Description 2"),
(3,"Test Fleet 3","Test Fleet Description 3")])
@pytest.mark.asyncio
async def test_get_fleet_by_id(id, name, description,test_session):
    response = await get_obj(Fleet,test_session,id)
    assert response.id == id
    assert response.name == name
    assert response.description == description

# Test get an vehicle
@pytest.mark.parametrize("id, name, description,fleet_id",
[(1,"Test Vehicle 1","Test Vehicle Description 1",1),
(2,"Test Vehicle 2","Test Vehicle Description 2",2),
(3,"Test Vehicle 3","Test Vehicle Description 3",3)])
@pytest.mark.asyncio
async def test_get_vehicle_by_id(id, name, description,fleet_id,test_session):
    response = await get_obj(Vehicle,test_session,id)
    assert response.id == id
    assert response.name == name
    assert response.description == description
    assert response.fleet_id == fleet_id

# Test get an driver
@pytest.mark.parametrize("name,age,id", [
    ("Test Driver 1", '1988-05-13',1),
    ("Test Driver 2", '1984-03-09',2),
    ("Test Driver 3", '1987-06-09',3)])
@pytest.mark.asyncio
async def test_get_driver_by_id(name, age, id,test_session):
    response = await get_obj(Driver,test_session,id)
    assert response.id == id
    assert response.name == name
    assert response.age == string_to_date(age)

# Test get an route
@pytest.mark.parametrize("id,name,description",
[(1,"Test Route 1","Test Route Description 1"),
(2,"Test Route 2","Test Route Description 2"),
(3,"Test Route 3","Test Route Description 3")])
@pytest.mark.asyncio
async def test_get_route_by_id(id, name, description,test_session):
    response = await get_obj(Route,test_session,id)
    assert response.id == id
    assert response.name == name
    assert response.description == description

# Test get an route detail
@pytest.mark.parametrize("route_id,driver_id,vehicle_id,start_time,end_time,start_location,end_location,ticket_price", [
    ("1", "1", "1", "2020-01-01T00:00:00Z", "2020-01-01T00:00:00Z", "Test Start Location 1", "Test End Location 1", 10),
    ("2", "2", "2", "2020-01-01T00:00:00Z", "2020-01-01T00:00:00Z", "Test Start Location 2", "Test End Location 2", 20),
    ("3", "3", "3", "2020-01-01T00:00:00Z", "2020-01-01T00:00:00Z", "Test Start Location 3", "Test End Location 3", 30),
    ("1", "2", "2", "2020-01-01T00:00:00Z", "2020-01-01T00:00:00Z", "Test Start Location 4", "Test End Location 4", 40),
    ("2", "3", "3", "2020-01-01T00:00:00Z", "2020-01-01T00:00:00Z", "Test Start Location 5", "Test End Location 5", 50),
    ("3", "1", "1", "2020-01-01T00:00:00Z", "2020-01-01T00:00:00Z", "Test Start Location 6", "Test End Location 6", 60),
    ("1", "3", "3", "2020-01-01T00:00:00Z", "2020-01-01T00:00:00Z", "Test Start Location 7", "Test End Location 7", 70),
    ("2", "1", "1", "2020-01-01T00:00:00Z", "2020-01-01T00:00:00Z", "Test Start Location 8", "Test End Location 8", 80),
    ("3", "2", "2", "2020-01-01T00:00:00Z", "2020-01-01T00:00:00Z", "Test Start Location 9", "Test End Location 9", 90)])
@pytest.mark.asyncio
async def test_get_route_detail_by_id(route_id, driver_id, vehicle_id, start_time, end_time, start_location, end_location, ticket_price,test_session):
    response = await get_obj(RouteDetail,test_session,route_id)
    assert response.route_id == route_id
    assert response.driver_id == driver_id
    assert response.vehicle_id == vehicle_id
    assert response.start_time == datetime.strptime(start_time,"%Y-%m-%dT%H:%M:%SZ")
    assert response.end_time == datetime.strptime(end_time,"%Y-%m-%dT%H:%M:%SZ")
    assert response.start_location == start_location
    assert response.end_location == end_location
    assert response.ticket_price == ticket_price

# Test update an object

# Test update a fleet
@pytest.mark.parametrize("id, name, description",
[(1,"Test Fleet 1","Test Fleet Description 1"),
(2,"Test Fleet 2","Test Fleet Description 2"),
(3,"Test Fleet 3","Test Fleet Description 3")])
@pytest.mark.asyncio
async def test_update_fleet_by_id(id, name, description,test_session):
    name = name + " Updated"
    fleet = FleetBase(name=name,description=description)
    response = await update_obj(Fleet,test_session,id, **fleet.dict())
    assert response == "Update Successfully"
    
# Test update a vehicle
@pytest.mark.parametrize("id, name, description,fleet id",
                         [(1,"Test Vehicle 1","Test Vehicle Description 1",1),
                          (2,"Test Vehicle 2","Test Vehicle Description 2",2),
                          (3,"Test Vehicle 3","Test Vehicle Description 3",3)])
@pytest.mark.asyncio
async def test_update_vehicle_by_id(id,name,description,fleet_id,test_session):
    name = name + " Updated"
    
    



# Test delete an object

# Test delete an fleet
@pytest.mark.parametrize("id", [1,2,3])
@pytest.mark.asyncio
async def test_delete_fleet_by_id(id,test_session):
    response = await delete_obj(cls = Fleet,session = test_session,id=id)
    assert response == "Deleted Successfully"

# Test delete an vehicle
@pytest.mark.parametrize("id", [1,2,3])
@pytest.mark.asyncio
async def test_delete_vehicle_by_id(id,test_session):
    response = await delete_obj(cls = Vehicle,session = test_session,id=id)
    assert response == "Deleted Successfully"

# Test delete an driver
@pytest.mark.parametrize("id", [1,2,3])
@pytest.mark.asyncio
async def test_delete_driver_by_id(id,test_session):
    response = await delete_obj(cls = Driver,session = test_session,id=id)
    assert response == "Deleted Successfully"

# Test delete an route
@pytest.mark.parametrize("id", [1,2,3])
@pytest.mark.asyncio
async def test_delete_route_by_id(id,test_session):
    response = await delete_obj(cls = Route,session = test_session,id=id)
    assert response == "Deleted Successfully"

# Test delete an route detail
@pytest.mark.parametrize("route_id,vehicle_id", 
[(1,1),(1,2),(1,3),(2,1),(2,2),(2,3),(3,1),(3,2),(3,3)])
@pytest.mark.asyncio
async def test_delete_route_detail_by_id(route_id,vehicle_id,test_session):
    response = await delete_route_detail(cls = RouteDetail,session = test_session,route_id=route_id,vehicle_id=vehicle_id)
    assert response == "Deleted Successfully"