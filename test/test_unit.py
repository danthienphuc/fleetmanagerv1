from datetime import date, datetime
from re import A
from typing import AsyncGenerator, Generator
from asyncio import current_task
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    AsyncEngine,
    async_scoped_session,
)
import pytest
from ..src.controller import *
from ..src import schemas, settings

@pytest.fixture()
def test_engine() -> Generator[AsyncEngine, None, None]:
    engine = create_async_engine(
        settings.db_url,
        echo=settings.db_echo,
        # pool_size=20, max_overflow=0
    )
    yield engine




@pytest.fixture()
async def test_session(test_engine: AsyncEngine) -> AsyncGenerator[AsyncSession, None]:

    # expire_on_commit=False will prevent attributes from being expired
    # after commit.
    session_maker = sessionmaker(
        bind=test_engine, expire_on_commit=False, class_=AsyncSession
    )
    Session = async_scoped_session(session_maker, scopefunc=current_task)
    async with Session() as session:
        yield session


# Refesh the database before testing.
@pytest.mark.refresh_db
@pytest.mark.asyncio
async def test_refresh_db(test_engine: AsyncEngine) -> None:
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        

# Test Create

# Test Create Fleet
@pytest.mark.create
@pytest.mark.fleet
@pytest.mark.parametrize(
    "name, description,id",
    [
        ("Test Fleet 1", "Test Fleet Description 1", 1),
        ("Test Fleet 2", "Test Fleet Description 2", 2),
        ("Test Fleet 3", "Test Fleet Description 3", 3),
    ],
)
@pytest.mark.asyncio
async def test_create_fleet(
    name: str, description: str, id: int, test_session: AsyncSession
) -> None:
    fleet = schemas.FleetCreate(name=name, description=description)
    response = await create_obj(Fleet, test_session, **fleet.dict())
    assert response.id == id
    assert response.name == name
    assert response.description == description


# Test create fleet with same name
@pytest.mark.create
@pytest.mark.fleet
@pytest.mark.parametrize(
    "name, description,id", [("Test Fleet 2", "Test Fleet Description 2", 2)]
)
@pytest.mark.asyncio
async def test_create_fleet_with_same_name(
    name: str, description: str, id: int, test_session: AsyncSession
) -> None:
    fleet = schemas.FleetCreate(name=name, description=description)
    response = await create_obj(Fleet, test_session, **fleet.dict())
    assert response.id == id
    assert response.name == name
    assert response.description == description


# Test create fleet with None name raise an error
@pytest.mark.create
@pytest.mark.fleet
@pytest.mark.parametrize(
    "name, description,id", [(None, "Test Fleet Description 5", 5)]
)
async def test_create_fleet_with_none_name(
    name: str, description: str, id: int, test_session: AsyncSession
) -> None:
    with pytest.raises(ValueError):
        fleet = schemas.FleetCreate(name=name, description=description)
        await create_obj(Fleet, test_session, **fleet.dict())


# Test create fleet with None description
@pytest.mark.create
@pytest.mark.fleet
@pytest.mark.parametrize("name, description,id", [("Test Fleet 4", None, 4)])
async def test_create_fleet_with_none_description(
    name: str, description: str, id: int, test_session: AsyncSession
) -> None:
    fleet = schemas.FleetCreate(name=name, description=description)
    response = await create_obj(Fleet, test_session, **fleet.dict())
    assert response.id == id
    assert response.name == name
    assert response.description == description


# Test create fleet with None name and None description raise error
@pytest.mark.create
@pytest.mark.fleet
@pytest.mark.parametrize("name, description,id", [(None, None, 6)])
async def test_create_fleet_with_none_name_and_none_description(
    name: str, description: str, id: int, test_session: AsyncSession
) -> None:
    with pytest.raises(ValueError):
        fleet = schemas.FleetCreate(name=name, description=description)
        await create_obj(Fleet, test_session, **fleet.dict())


# Test Create Vehicle
@pytest.mark.create
@pytest.mark.vehicle
@pytest.mark.parametrize(
    "name, description,fleet_id,id",
    [
        ("Test Vehicle 1", "Test Vehicle Description 1", 1, 1),
        ("Test Vehicle 2", "Test Vehicle Description 2", 2, 2),
        ("Test Vehicle 3", "Test Vehicle Description 3", 3, 3),
    ],
)
@pytest.mark.asyncio
async def test_create_vehicle(
    name: str, description: str, fleet_id: int, id: int, test_session: AsyncSession
) -> None:
    vehicle = schemas.VehicleCreate(
        name=name, description=description, fleet_id=fleet_id
    )
    response = await create_obj(Vehicle, test_session, **vehicle.dict())
    assert response.id == id
    assert response.name == name
    assert response.description == description
    assert response.fleet_id == fleet_id


# Test create vehicle with same name
@pytest.mark.create
@pytest.mark.vehicle
@pytest.mark.parametrize(
    "name, description,fleet_id,id",
    [("Test Vehicle 4", "Test Vehicle Description 4", 4, 4)],
)
@pytest.mark.asyncio
async def test_create_vehicle_with_same_name(
    name: str, description: str, fleet_id: int, id: int, test_session: AsyncSession
) -> None:
    vehicle = schemas.VehicleCreate(
        name=name, description=description, fleet_id=fleet_id
    )
    response = await create_obj(Vehicle, test_session, **vehicle.dict())
    assert response.id == id
    assert response.name == name
    assert response.description == description
    assert response.fleet_id == fleet_id

# Test create vehicle with None name raise an error
@pytest.mark.create
@pytest.mark.vehicle
@pytest.mark.parametrize(
    "name, description,fleet_id,id", [(None, "Test Vehicle Description 5", 1, 5)]
)
async def test_create_vehicle_with_none_name(
    name: str, description: str, fleet_id: int, id: int, test_session: AsyncSession
) -> None:
    with pytest.raises(ValueError):
        vehicle = schemas.VehicleCreate(
            name=name, description=description, fleet_id=fleet_id
        )
        await create_obj(Vehicle, test_session, **vehicle.dict())


# Test create vehicle with None description
@pytest.mark.create
@pytest.mark.vehicle
@pytest.mark.parametrize(
    "name, description,fleet_id,id", [("Test Vehicle 5", None, 4, 5)]
)
async def test_create_vehicle_with_none_description(
    name: str, description: str, fleet_id: int, id: int, test_session: AsyncSession
) -> None:
    vehicle = schemas.VehicleCreate(
        name=name, description=description, fleet_id=fleet_id
    )
    response = await create_obj(Vehicle, test_session, **vehicle.dict())
    assert response.id == id
    assert response.name == name
    assert response.description == description
    assert response.fleet_id == fleet_id


# Test create vehicle with None fleet_id raise an error
@pytest.mark.create
@pytest.mark.vehicle
@pytest.mark.parametrize(
    "name, description,fleet_id,id",
    [("Test Vehicle 6", "Test Vehicle Description 6", None, 6)],
)
async def test_create_vehicle_with_none_fleet_id(
    name: str, description: str, fleet_id: int, id: int, test_session: AsyncSession
) -> None:
    with pytest.raises(ValueError):
        vehicle = schemas.VehicleCreate(
            name=name, description=description, fleet_id=fleet_id
        )
        await create_obj(Vehicle, test_session, **vehicle.dict())


# Test create vehicle with None name, None description and None fleet_id raise error
@pytest.mark.create
@pytest.mark.vehicle
@pytest.mark.parametrize("name, description,fleet_id,id", [(None, None, None, 6)])
async def test_create_vehicle_with_none_name_and_none_description(
    name: str, description: str, fleet_id: int, id: int, test_session: AsyncSession
) -> None:
    with pytest.raises(ValueError):
        vehicle = schemas.VehicleCreate(
            name=name, description=description, fleet_id=fleet_id
        )
        await create_vehicle_obj(test_session, **vehicle.dict())


# Test create vehicle with fleet_id not exist
@pytest.mark.create
@pytest.mark.vehicle
@pytest.mark.parametrize(
    "name, description,fleet_id,id",
    [("Test Vehicle 7", "Test Vehicle Description 7", 99, 6)],
)
async def test_create_vehicle_with_fleet_id_not_exist(
    name: str, description: str, fleet_id: int, id: int, test_session: AsyncSession
) -> None:
    with pytest.raises(IntegrityError):
        vehicle = schemas.VehicleCreate(
            name=name, description=description, fleet_id=fleet_id
        )
        await create_obj(Vehicle, test_session, **vehicle.dict())


# Test Create Driver
@pytest.mark.create
@pytest.mark.driver
@pytest.mark.parametrize(
    "name,age,id",
    [
        ("Test Driver 1", "1988-05-13", 1),
        ("Test Driver 2", "1984-03-09", 2),
        ("Test Driver 3", "1987-06-09", 3),
    ],
)
@pytest.mark.asyncio
async def test_create_driver(
    name: str, age: str, id: int, test_session: AsyncSession
) -> None:
    driver = schemas.DriverCreate(name=name, age=datetime.strptime(age, "%Y-%m-%d"))
    response = await create_obj(Driver, test_session, **driver.dict())
    assert response.id == id
    assert response.name == name
    assert response.age == datetime.strptime(age, "%Y-%m-%d").date()


# Test create driver with same name
@pytest.mark.create
@pytest.mark.driver
@pytest.mark.parametrize("name,age,id", [("Test Driver 4", "1988-05-13", 4)])
@pytest.mark.asyncio
async def test_create_driver_with_same_name(
    name: str, age: str, id: int, test_session: AsyncSession
) -> None:
    driver = schemas.DriverCreate(name=name, age=datetime.strptime(age, "%Y-%m-%d"))
    response = await create_obj(Driver, test_session, **driver.dict())
    assert response.id == id
    assert response.name == name
    assert response.age == datetime.strptime(age, "%Y-%m-%d").date()


# Test create driver with None name raise an error
@pytest.mark.create
@pytest.mark.driver
@pytest.mark.parametrize("name,age,id", [(None, "1988-05-13", 5)])
async def test_create_driver_with_none_name(
    name: str, age: str, id: int, test_session: AsyncSession
) -> None:
    with pytest.raises(ValueError):
        driver = schemas.DriverCreate(name=name, age=datetime.strptime(age, "%Y-%m-%d"))
        await create_obj(Driver, test_session, **driver.dict())


# Test create driver with None age raise an error
@pytest.mark.create
@pytest.mark.driver
@pytest.mark.parametrize("name,age,id", [("Test Driver 6", None, 6)])
async def test_create_driver_with_none_age(
    name: str, age: str, id: int, test_session: AsyncSession
) -> None:
    with pytest.raises(TypeError):
        driver = schemas.DriverCreate(name=name, age=datetime.strptime(age, "%Y-%m-%d"))
        await create_obj(Driver, test_session, **driver.dict())


# Test Create Driver with None name, None age raise error
@pytest.mark.create
@pytest.mark.driver
@pytest.mark.parametrize("name,age,id", [(None, None, 6)])
async def test_create_driver_with_none_name_and_none_age(
    name: str, age: str, id: int, test_session: AsyncSession
) -> None:
    with pytest.raises(TypeError):
        driver = schemas.DriverCreate(name=name, age=datetime.strptime(age, "%Y-%m-%d"))
        await create_obj(Driver, test_session, **driver.dict())


# Test Create Route
@pytest.mark.create
@pytest.mark.route
@pytest.mark.parametrize(
    "name, description,id",
    [
        ("Test Route 1", "Test Route Description 1", 1),
        ("Test Route 2", "Test Route Description 2", 2),
        ("Test Route 3", "Test Route Description 3", 3),
    ],
)
@pytest.mark.asyncio
async def test_create_route(
    name: str, description: str, id: int, test_session: AsyncSession
) -> None:
    route = schemas.RouteCreate(name=name, description=description)
    response = await create_obj(Route, test_session, **route.dict())
    assert response.id == id
    assert response.name == name
    assert response.description == description


# Test create route with same name
@pytest.mark.create
@pytest.mark.route
@pytest.mark.parametrize(
    "name, description,id", [("Test Route 4", "Test Route Description 4", 4)]
)
@pytest.mark.asyncio
async def test_create_route_with_same_name(
    name: str, description: str, id: int, test_session: AsyncSession
) -> None:
    route = schemas.RouteCreate(name=name, description=description)
    response = await create_obj(Route, test_session, **route.dict())
    assert response.id == id
    assert response.name == name
    assert response.description == description


# Test create route with None name raise an error
@pytest.mark.create
@pytest.mark.route
@pytest.mark.parametrize(
    "name, description,id", [(None, "Test Route Description 5", 5)]
)
async def test_create_route_with_none_name(
    name: str, description: str, id: int, test_session: AsyncSession
) -> None:
    with pytest.raises(ValueError):
        route = schemas.RouteCreate(name=name, description=description)
        await create_obj(Route, test_session, **route.dict())


# Test create route with None description
@pytest.mark.create
@pytest.mark.route
@pytest.mark.parametrize("name, description,id", [("Test Route 5", None, 5)])
async def test_create_route_with_none_description(
    name: str, description: str, id: int, test_session: AsyncSession
) -> None:
    route = schemas.RouteCreate(name=name, description=description)
    response = await create_obj(Route, test_session, **route.dict())
    assert response.id == id
    assert response.name == name
    assert response.description == description


# Test create route with None name, None description raise error
@pytest.mark.create
@pytest.mark.route
@pytest.mark.parametrize("name, description,id", [(None, None, 6)])
async def test_create_route_with_none_name_and_none_description(
    name: str, description: str, id: int, test_session: AsyncSession
) -> None:
    with pytest.raises(ValueError):
        route = schemas.RouteCreate(name=name, description=description)
        await create_obj(Route, test_session, **route.dict())


# Test Create Route Detail
@pytest.mark.create
@pytest.mark.route_detail
@pytest.mark.parametrize(
    "route_id,driver_id,vehicle_id,start_time,end_time,start_location,end_location,ticket_price",
    [
        (
            1,
            1,
            1,
            "2020-01-01T00:00:00Z",
            "2020-01-01T00:00:00Z",
            "Test Start Location 1",
            "Test End Location 1",
            10,
        ),
        (
            2,
            2,
            2,
            "2020-01-01T00:00:00Z",
            "2020-01-01T00:00:00Z",
            "Test Start Location 2",
            "Test End Location 2",
            20,
        ),
        (
            3,
            3,
            3,
            "2020-01-01T00:00:00Z",
            "2020-01-01T00:00:00Z",
            "Test Start Location 3",
            "Test End Location 3",
            30,
        ),
    ],
)
@pytest.mark.asyncio
async def test_create_route_details(
    route_id: int,
    driver_id: int,
    vehicle_id: int,
    start_time: str,
    end_time: str,
    start_location: str,
    end_location: str,
    ticket_price: int,
    test_session: AsyncSession,
) -> None:
    route_detail = schemas.RouteDetailCreate(
        route_id=route_id,
        driver_id=driver_id,
        vehicle_id=vehicle_id,
        start_time=datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%SZ"),
        end_time=datetime.strptime(end_time, "%Y-%m-%dT%H:%M:%SZ"),
        start_location=start_location,
        end_location=end_location,
        ticket_price=ticket_price,
    )
    response = await create_obj_db(RouteDetail, test_session, **route_detail.dict())
    assert response.route_id == route_id
    assert response.driver_id == driver_id
    assert response.vehicle_id == vehicle_id
    assert response.start_time == datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%SZ")
    assert response.end_time == datetime.strptime(end_time, "%Y-%m-%dT%H:%M:%SZ")
    assert response.start_location == start_location
    assert response.end_location == end_location
    assert response.ticket_price == ticket_price


# Test Create Route Detail with None route_id raise error
@pytest.mark.create
@pytest.mark.route_detail
@pytest.mark.parametrize(
    "route_id,driver_id,vehicle_id,start_time,end_time,start_location,end_location,ticket_price",
    [
        (
            None,
            1,
            1,
            "2020-01-01T00:00:00Z",
            "2020-01-01T00:00:00Z",
            "Test Start Location 1",
            "Test End Location 1",
            10,
        )
    ],
)
async def test_create_route_detail_with_none_route_id(
    route_id: int,
    driver_id: int,
    vehicle_id: int,
    start_time: str,
    end_time: str,
    start_location: str,
    end_location: str,
    ticket_price: int,
    test_session: AsyncSession,
) -> None:
    with pytest.raises(ValueError):
        route_detail = schemas.RouteDetailCreate(
            route_id=route_id,
            driver_id=driver_id,
            vehicle_id=vehicle_id,
            start_time=datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%SZ"),
            end_time=datetime.strptime(end_time, "%Y-%m-%dT%H:%M:%SZ"),
            start_location=start_location,
            end_location=end_location,
            ticket_price=ticket_price,
        )
        await create_obj(RouteDetail, test_session, **route_detail.dict())


# Test Create Route Detail with None driver_id raise error
@pytest.mark.create
@pytest.mark.route_detail
@pytest.mark.parametrize(
    "route_id,vehicle_id,driver_id,start_time,end_time,start_location,end_location,ticket_price",
    [
        (
            1,
            1,
            None,
            "2020-01-01T00:00:00Z",
            "2020-01-01T00:00:00Z",
            "Test Start Location 1",
            "Test End Location 1",
            10,
        )
    ],
)
async def test_create_route_detail_with_none_driver_id(
    route_id: int,
    driver_id: int,
    vehicle_id: int,
    start_time: str,
    end_time: str,
    start_location: str,
    end_location: str,
    ticket_price: int,
    test_session: AsyncSession,
) -> None:
    with pytest.raises(ValueError):
        route_detail = schemas.RouteDetailCreate(
            route_id=route_id,
            driver_id=driver_id,
            vehicle_id=vehicle_id,
            start_time=datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%SZ"),
            end_time=datetime.strptime(end_time, "%Y-%m-%dT%H:%M:%SZ"),
            start_location=start_location,
            end_location=end_location,
            ticket_price=ticket_price,
        )
        await create_obj(RouteDetail, test_session, **route_detail.dict())


# Test Create Route Detail with None start_time raise error
@pytest.mark.create
@pytest.mark.route_detail
@pytest.mark.parametrize(
    "route_id,vehicle_id,driver_id,start_time,end_time,start_location,end_location,ticket_price",
    [
        (
            1,
            2,
            1,
            None,
            "2020-01-01T00:00:00Z",
            "Test Start Location 1",
            "Test End Location 1",
            10,
        )
    ],
)
async def test_create_route_detail_with_none_start_time(
    route_id: int,
    driver_id: int,
    vehicle_id: int,
    start_time: str,
    end_time: str,
    start_location: str,
    end_location: str,
    ticket_price: int,
    test_session: AsyncSession,
) -> None:
    with pytest.raises(ValueError):
        route_detail = schemas.RouteDetailCreate(
            route_id=route_id,
            driver_id=driver_id,
            vehicle_id=vehicle_id,
            start_time=start_time,
            end_time=datetime.strptime(end_time, "%Y-%m-%dT%H:%M:%SZ"),
            start_location=start_location,
            end_location=end_location,
            ticket_price=ticket_price,
        )
        await create_obj(RouteDetail, test_session, **route_detail.dict())


# Test Create Route Detail with start_time is another date format raise error
@pytest.mark.create
@pytest.mark.route_detail
@pytest.mark.parametrize(
    "route_id,driver_id,vehicle_id,start_time,end_time,start_location,end_location,ticket_price",
    [
        (
            1,
            3,
            1,
            "2020-01-01 00:00:00",
            "2020-01-01T00:00:00Z",
            "Test Start Location 1",
            "Test End Location 1",
            10,
        )
    ],
)
async def test_create_route_detail_with_start_time_is_another_date_format(
    route_id: int,
    driver_id: int,
    vehicle_id: int,
    start_time: str,
    end_time: str,
    start_location: str,
    end_location: str,
    ticket_price: int,
    test_session: AsyncSession,
) -> None:
    with pytest.raises(ValueError):
        route_detail = schemas.RouteDetailCreate(
            route_id=route_id,
            driver_id=driver_id,
            vehicle_id=vehicle_id,
            start_time=datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%SZ"),
            end_time=datetime.strptime(end_time, "%Y-%m-%dT%H:%M:%SZ"),
            start_location=start_location,
            end_location=end_location,
            ticket_price=ticket_price,
        )
        await create_obj(RouteDetail, test_session, **route_detail.dict())


# Test Create Route Detail with start_time have not time
@pytest.mark.create
@pytest.mark.route_detail
@pytest.mark.parametrize(
    "route_id,driver_id,vehicle_id,start_time,end_time,start_location,end_location,ticket_price",
    [
        (
            1,
            3,
            1,
            "2020-01-01",
            "2020-01-01T00:00:00Z",
            "Test Start Location 1",
            "Test End Location 1",
            10,
        )
    ],
)
async def test_create_route_detail_with_start_time_have_not_time(
    route_id: int,
    driver_id: int,
    vehicle_id: int,
    start_time: str,
    end_time: str,
    start_location: str,
    end_location: str,
    ticket_price: int,
    test_session: AsyncSession,
) -> None:
    with pytest.raises(ValueError):
        route_detail = schemas.RouteDetailCreate(
            route_id=route_id,
            driver_id=driver_id,
            vehicle_id=vehicle_id,
            start_time=datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%SZ"),
            end_time=datetime.strptime(end_time, "%Y-%m-%dT%H:%M:%SZ"),
            start_location=start_location,
            end_location=end_location,
            ticket_price=ticket_price,
        )
        await create_obj(RouteDetail, test_session, **route_detail.dict())


# Test Create Route Detail with route_id is not int raise error
@pytest.mark.create
@pytest.mark.route_detail
@pytest.mark.parametrize(
    "route_id,driver_id,vehicle_id,start_time,end_time,start_location,end_location,ticket_price",
    [
        (
            "1",
            3,
            1,
            "2020-01-01T00:00:00Z",
            "2020-01-01T00:00:00Z",
            "Test Start Location 1",
            "Test End Location 1",
            10,
        )
    ],
)
async def test_create_route_detail_with_route_id_is_not_int(
    route_id: int,
    driver_id: int,
    vehicle_id: int,
    start_time: str,
    end_time: str,
    start_location: str,
    end_location: str,
    ticket_price: int,
    test_session: AsyncSession,
) -> None:
    with pytest.raises(IntegrityError):
        route_detail = schemas.RouteDetailCreate(
            route_id=route_id,
            driver_id=driver_id,
            vehicle_id=vehicle_id,
            start_time=datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%SZ"),
            end_time=datetime.strptime(end_time, "%Y-%m-%dT%H:%M:%SZ"),
            start_location=start_location,
            end_location=end_location,
            ticket_price=ticket_price,
        )
        await create_obj_db(RouteDetail, test_session, **route_detail.dict())


# Test Create Route Detail with route_id is negative raise error
@pytest.mark.create
@pytest.mark.route_detail
@pytest.mark.parametrize(
    "route_id,driver_id,vehicle_id,start_time,end_time,start_location,end_location,ticket_price",
    [
        (
            -1,
            3,
            1,
            "2020-01-01T00:00:00Z",
            "2020-01-01T00:00:00Z",
            "Test Start Location 1",
            "Test End Location 1",
            10,
        )
    ],
)
async def test_create_route_detail_with_route_id_is_negative(
    route_id: int,
    driver_id: int,
    vehicle_id: int,
    start_time: str,
    end_time: str,
    start_location: str,
    end_location: str,
    ticket_price: int,
    test_session: AsyncSession,
) -> None:
    with pytest.raises(IntegrityError):
        route_detail = schemas.RouteDetailCreate(
            route_id=route_id,
            driver_id=driver_id,
            vehicle_id=vehicle_id,
            start_time=datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%SZ"),
            end_time=datetime.strptime(end_time, "%Y-%m-%dT%H:%M:%SZ"),
            start_location=start_location,
            end_location=end_location,
            ticket_price=ticket_price,
        )
        await create_obj_db(RouteDetail, test_session, **route_detail.dict())


# Test get all objects

# Test get all fleets
@pytest.mark.get_all
@pytest.mark.fleet
@pytest.mark.asyncio
async def test_get_all_fleets(test_session: AsyncSession) -> None:
    response = await get_all_obj(Fleet, test_session, None)
    assert len(response) == 4
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
@pytest.mark.get_all
@pytest.mark.vehicle
@pytest.mark.asyncio
async def test_get_all_vehicles(test_session: AsyncSession) -> None:
    response = await get_all_obj(Vehicle, test_session, None)
    assert len(response) == 5
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
@pytest.mark.get_all
@pytest.mark.driver
@pytest.mark.asyncio
async def test_get_all_drivers(test_session: AsyncSession) -> None:
    response = await get_all_obj(Driver, test_session, None)
    assert len(response) == 4
    assert response[0].id == 1
    assert response[0].name == "Test Driver 1"
    assert response[0].age == datetime.strptime("1988-05-13", "%Y-%m-%d").date()
    assert response[1].id == 2
    assert response[1].name == "Test Driver 2"
    assert response[1].age == datetime.strptime("1984-03-09", "%Y-%m-%d").date()
    assert response[2].id == 3
    assert response[2].name == "Test Driver 3"
    assert response[2].age == datetime.strptime("1987-06-09", "%Y-%m-%d").date()


# Test get all routes
@pytest.mark.get_all
@pytest.mark.route
@pytest.mark.asyncio
async def test_get_all_routes(test_session: AsyncSession) -> None:
    response = await get_all_obj(Route, test_session, None)
    assert len(response) == 5
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
@pytest.mark.get_all
@pytest.mark.route_detail
@pytest.mark.asyncio
async def test_get_all_route_details(test_session: AsyncSession) -> None:
    response = await get_all_obj(RouteDetail, test_session, None)
    assert len(response) == 3
    assert response[0].route_id == 1
    assert response[0].driver_id == 1
    assert response[0].vehicle_id == 1
    assert response[0].start_time == datetime.strptime(
        "2020-01-01T00:00:00Z", "%Y-%m-%dT%H:%M:%SZ"
    )
    assert response[0].end_time == datetime.strptime(
        "2020-01-01T00:00:00Z", "%Y-%m-%dT%H:%M:%SZ"
    )
    assert response[0].start_location == "Test Start Location 1"
    assert response[0].end_location == "Test End Location 1"
    assert response[0].ticket_price == 10
    assert response[1].route_id == 2
    assert response[1].driver_id == 2
    assert response[1].vehicle_id == 2
    assert response[1].start_time == datetime.strptime(
        "2020-01-01T00:00:00Z", "%Y-%m-%dT%H:%M:%SZ"
    )
    assert response[1].end_time == datetime.strptime(
        "2020-01-01T00:00:00Z", "%Y-%m-%dT%H:%M:%SZ"
    )
    assert response[1].start_location == "Test Start Location 2"
    assert response[1].end_location == "Test End Location 2"
    assert response[1].ticket_price == 20
    assert response[2].route_id == 3
    assert response[2].driver_id == 3
    assert response[2].vehicle_id == 3
    assert response[2].start_time == datetime.strptime(
        "2020-01-01T00:00:00Z", "%Y-%m-%dT%H:%M:%SZ"
    )
    assert response[2].end_time == datetime.strptime(
        "2020-01-01T00:00:00Z", "%Y-%m-%dT%H:%M:%SZ"
    )
    assert response[2].start_location == "Test Start Location 3"
    assert response[2].end_location == "Test End Location 3"
    assert response[2].ticket_price == 30


# Test get by name

# Test get fleet by name
@pytest.mark.fleet
@pytest.mark.asyncio
async def test_get_fleet_by_name(test_session: AsyncSession) -> None:
    response = await get_all_obj(Fleet, test_session, "Test Fleet 1")
    assert response[0].id == 1
    assert response[0].name == "Test Fleet 1"
    assert response[0].description == "Test Fleet Description 1"


# Test get fleet by characters in name
@pytest.mark.get_by_name
@pytest.mark.fleet
@pytest.mark.asyncio
async def test_get_fleet_by_characters_in_name(test_session: AsyncSession) -> None:
    response = await get_all_obj(Fleet, test_session, "Fleet 1")
    assert response[0].id == 1
    assert response[0].name == "Test Fleet 1"
    assert response[0].description == "Test Fleet Description 1"


# Test get fleet by nomalize characters not in name
@pytest.mark.get_by_name
@pytest.mark.fleet
@pytest.mark.asyncio
async def test_get_fleet_by_normalize_characters_not_in_name(
    test_session: AsyncSession,
) -> None:
    response = await get_all_obj(Fleet, test_session, "not in name")
    assert len(response) == 0


# Test get fleet by special characters not in name
@pytest.mark.get_by_name
@pytest.mark.fleet
@pytest.mark.asyncio
async def test_get_fleet_by_special_characters_not_in_name(
    test_session: AsyncSession,
) -> None:
    response = await get_all_obj(Fleet, test_session, "!@#$%^&*()_+-={}[];':,./<>?|")
    assert len(response) == 0


# Test get an object by id

# Test get an fleet
@pytest.mark.get
@pytest.mark.fleet
@pytest.mark.parametrize(
    "id, name, description",
    [
        (1, "Test Fleet 1", "Test Fleet Description 1"),
        (2, "Test Fleet 2", "Test Fleet Description 2"),
        (3, "Test Fleet 3", "Test Fleet Description 3"),
    ],
)
@pytest.mark.asyncio
async def test_get_fleet_by_id(
    id: int, name: str, description: str, test_session: AsyncSession
) -> None:
    response = await get_obj(Fleet, test_session, id)
    assert response.id == id
    assert response.name == name
    assert response.description == description


# Test get an vehicle
@pytest.mark.get
@pytest.mark.vehicle
@pytest.mark.parametrize(
    "id, name, description,fleet_id",
    [
        (1, "Test Vehicle 1", "Test Vehicle Description 1", 1),
        (2, "Test Vehicle 2", "Test Vehicle Description 2", 2),
        (3, "Test Vehicle 3", "Test Vehicle Description 3", 3),
    ],
)
@pytest.mark.asyncio
async def test_get_vehicle_by_id(
    id: int, name: str, description: str, fleet_id: int, test_session: AsyncSession
) -> None:
    response = await get_obj(Vehicle, test_session, id)
    assert response.id == id
    assert response.name == name
    assert response.description == description
    assert response.fleet_id == fleet_id


# Test get an driver
@pytest.mark.get
@pytest.mark.driver
@pytest.mark.parametrize(
    "name,age,id",
    [
        ("Test Driver 1", "1988-05-13", 1),
        ("Test Driver 2", "1984-03-09", 2),
        ("Test Driver 3", "1987-06-09", 3),
    ],
)
@pytest.mark.asyncio
async def test_get_driver_by_id(
    name: str, age: str, id: int, test_session: AsyncSession
) -> None:
    response = await get_obj(Driver, test_session, id)
    assert response.id == id
    assert response.name == name
    assert response.age == datetime.strptime(age, "%Y-%m-%d").date()


# Test get an route
@pytest.mark.get
@pytest.mark.route
@pytest.mark.parametrize(
    "id,name,description",
    [
        (1, "Test Route 1", "Test Route Description 1"),
        (2, "Test Route 2", "Test Route Description 2"),
        (3, "Test Route 3", "Test Route Description 3"),
    ],
)
@pytest.mark.asyncio
async def test_get_route_by_id(
    id: int, name: str, description: str, test_session: AsyncSession
) -> None:
    response = await get_obj(Route, test_session, id)
    assert response.id == id
    assert response.name == name
    assert response.description == description


# Test get an route detail
@pytest.mark.get
@pytest.mark.route_detail
@pytest.mark.parametrize(
    "route_id,driver_id,vehicle_id,start_time,end_time,start_location,end_location,ticket_price",
    [
        (
            1,
            1,
            1,
            "2020-01-01T00:00:00Z",
            "2020-01-01T00:00:00Z",
            "Test Start Location 1",
            "Test End Location 1",
            10,
        ),
        (
            2,
            2,
            2,
            "2020-01-01T00:00:00Z",
            "2020-01-01T00:00:00Z",
            "Test Start Location 2",
            "Test End Location 2",
            20,
        ),
        (
            3,
            3,
            3,
            "2020-01-01T00:00:00Z",
            "2020-01-01T00:00:00Z",
            "Test Start Location 3",
            "Test End Location 3",
            30,
        ),
    ],
)
@pytest.mark.asyncio
async def test_get_route_detail_by_id(
    route_id: int,
    driver_id: int,
    vehicle_id: int,
    start_time: str,
    end_time: str,
    start_location: str,
    end_location: str,
    ticket_price: int,
    test_session: AsyncSession,
) -> None:
    response = await get_route_detail_obj(test_session, route_id, vehicle_id)
    assert response.route_id == route_id
    assert response.driver_id == driver_id
    assert response.vehicle_id == vehicle_id
    assert response.start_time == datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%SZ")
    assert response.end_time == datetime.strptime(end_time, "%Y-%m-%dT%H:%M:%SZ")
    assert response.start_location == start_location
    assert response.end_location == end_location
    assert response.ticket_price == ticket_price


# Test update an object

# Test update a fleet
@pytest.mark.update
@pytest.mark.fleet
@pytest.mark.parametrize(
    "id, name, description",
    [
        (1, "Test Fleet 1", "Test Fleet Description 1"),
        (2, "Test Fleet 2", "Test Fleet Description 2"),
        (3, "Test Fleet 3", "Test Fleet Description 3"),
    ],
)
@pytest.mark.asyncio
async def test_update_fleet_by_id(
    id: int, name: str, description: str, test_session: AsyncSession
) -> None:
    name = name + " Updated"
    fleet = schemas.FleetBase(name=name, description=description)
    response = await update_obj(Fleet, test_session, id, **fleet.dict())
    assert response == "Updated Successfully"


# Test update a vehicle
@pytest.mark.update
@pytest.mark.vehicle
@pytest.mark.parametrize(
    "id, name, description,fleet_id",
    [
        (1, "Test Vehicle 1", "Test Vehicle Description 1", 1),
        (2, "Test Vehicle 2", "Test Vehicle Description 2", 2),
        (3, "Test Vehicle 3", "Test Vehicle Description 3", 3),
    ],
)
@pytest.mark.asyncio
async def test_update_vehicle_by_id(
    id: int, name: str, description: str, fleet_id: int, test_session: AsyncSession
) -> None:
    name = name + " Updated"
    vehicle = schemas.VehicleBase(name=name, description=description, fleet_id=fleet_id)
    response = await update_obj(Vehicle, test_session, id, **vehicle.dict())
    assert response == "Updated Successfully"


# Test update a driver
@pytest.mark.update
@pytest.mark.driver
@pytest.mark.parametrize(
    "id, name, age",
    [
        (1, "Test Driver 1", "1988-05-13"),
        (2, "Test Driver 2", "1984-03-09"),
        (3, "Test Driver 3", "1987-06-09"),
    ],
)
@pytest.mark.asyncio
async def test_update_driver_by_id(
    id: int, name: str, age: str, test_session: AsyncSession
) -> None:
    name = name + " Updated"
    driver = schemas.DriverBase(name=name, age=datetime.strptime(age, "%Y-%m-%d"))
    response = await update_obj(Driver, test_session, id, **driver.dict())
    assert response == "Updated Successfully"


# Test update a route
@pytest.mark.update
@pytest.mark.route
@pytest.mark.parametrize(
    "id, name, description",
    [
        (1, "Test Route 1", "Test Route Description 1"),
        (2, "Test Route 2", "Test Route Description 2"),
        (3, "Test Route 3", "Test Route Description 3"),
    ],
)
@pytest.mark.asyncio
async def test_update_route_by_id(
    id: int, name: str, description: str, test_session: AsyncSession
) -> None:
    name = name + " Updated"
    route = schemas.RouteBase(name=name, description=description)
    response = await update_obj(Route, test_session, id, **route.dict())
    assert response == "Updated Successfully"


# Test update a route detail
@pytest.mark.update
@pytest.mark.route_detail
@pytest.mark.parametrize(
    "route_id,driver_id,vehicle_id,start_time,end_time,start_location,end_location,ticket_price",
    [
        (
            1,
            1,
            1,
            "2020-01-01T00:00:00Z",
            "2020-01-01T00:00:00Z",
            "Test Start Location 1",
            "Test End Location 1",
            10,
        ),
        (
            2,
            2,
            2,
            "2020-01-01T00:00:00Z",
            "2020-01-01T00:00:00Z",
            "Test Start Location 2",
            "Test End Location 2",
            20,
        ),
        (
            3,
            3,
            3,
            "2020-01-01T00:00:00Z",
            "2020-01-01T00:00:00Z",
            "Test Start Location 3",
            "Test End Location 3",
            30,
        ),
    ],
)
@pytest.mark.asyncio
async def test_update_route_detail_by_id(
    route_id: int,
    driver_id: int,
    vehicle_id: int,
    start_time: str,
    end_time: str,
    start_location: str,
    end_location: str,
    ticket_price: int,
    test_session: AsyncSession,
) -> None:
    route_detail = schemas.RouteDetailBase(
        driver_id=driver_id,
        start_time=datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%SZ"),
        end_time=datetime.strptime(end_time, "%Y-%m-%dT%H:%M:%SZ"),
        start_location=start_location,
        end_location=end_location,
        ticket_price=ticket_price,
    )
    route_detail.start_location = start_location + " Updated"
    route_detail.end_location = end_location + " Updated"
    response = await update_route_detail_obj(
        test_session, route_id, vehicle_id, **route_detail.dict()
    )
    assert response == "Updated Successfully"


# Test delete an object

# Test delete an route detail
@pytest.mark.delete
@pytest.mark.route_detail
@pytest.mark.parametrize("route_id,vehicle_id", [(1, 1), (2, 2), (3, 3)])
@pytest.mark.asyncio
async def test_delete_route_detail_by_id(
    route_id: int, vehicle_id: int, test_session: AsyncSession
) -> None:
    response = await delete_route_detail_obj(
        session=test_session, route_id=route_id, vehicle_id=vehicle_id
    )
    assert response == "Deleted Successfully"


# Test delete an vehicle
@pytest.mark.delete
@pytest.mark.vehicle
@pytest.mark.parametrize("id", [1, 2, 3])
@pytest.mark.asyncio
async def test_delete_vehicle_by_id(id: int, test_session: AsyncSession) -> None:
    response = await delete_obj(cls=Vehicle, session=test_session, id=id)
    assert response == "Deleted Successfully"


# Test delete an fleet
@pytest.mark.delete
@pytest.mark.fleet
@pytest.mark.parametrize("id", [1, 2, 3])
@pytest.mark.asyncio
async def test_delete_fleet_by_id(id: int, test_session: AsyncSession) -> None:
    response = await delete_obj(cls=Fleet, session=test_session, id=id)
    assert response == "Deleted Successfully"


# Test delete an driver
@pytest.mark.delete
@pytest.mark.driver
@pytest.mark.parametrize("id", [1, 2, 3])
@pytest.mark.asyncio
async def test_delete_driver_by_id(id: int, test_session: AsyncSession) -> None:
    response = await delete_obj(cls=Driver, session=test_session, id=id)
    assert response == "Deleted Successfully"


# Test delete an route
@pytest.mark.delete
@pytest.mark.route
@pytest.mark.parametrize("id", [1, 2, 3])
@pytest.mark.asyncio
async def test_delete_route_by_id(id: int, test_session: AsyncSession) -> None:
    response = await delete_obj(cls=Route, session=test_session, id=id)
    assert response == "Deleted Successfully"
