from typing import List
from unittest import result
from fastapi import Query
from sqlalchemy import join, update, delete
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from .models import *

# Create obj in database
async def create_obj_db(cls: Any, session: AsyncSession, **kwargs: Any) -> Any:
    obj = cls(**kwargs)
    session.add(obj)
    await session.commit()
    await session.refresh(obj)
    return obj

# Check name is exist or not when create object
async def create_obj(cls: Any, session: AsyncSession, **kwargs: Any) -> Any:
    results = await session.execute(select(cls).where(cls.name == kwargs["name"]))
    obj = results.scalar()
    if obj is None:
        obj = await create_obj_db(cls, session, **kwargs)
    return obj

# Get obj by id
async def get_obj(cls: Any, session: AsyncSession, id: int) -> Any:
    query = select(cls).where(cls.id == id)
    results = await session.execute(query)
    return results.scalar()

# Get all obj from database, if name is not None, get obj by name
async def get_all_obj(cls: Any, session: AsyncSession, name: str = Query(None)) -> Any:
    query = select(cls)
    if name is not None:
        query = query.filter(cls.name.like("%" + name + "%"))
    results = await session.execute(query)
    return results.scalars().all()

# Update obj in database
async def update_obj(cls: Any, session: AsyncSession, id: int, **kwargs: Any) -> str:
    # Check obj is exist or not
    obj = await get_obj(cls, session, id)
    if obj is None:
        return "Object not exist"
    query = (
        update(cls)
        .where(cls.id == id)
        .values(**kwargs)
        .execution_options(synchronize_session="fetch")
    )

    await session.execute(query)
    await session.commit()
    return "Updated Successfully"

# Delete obj from database
async def delete_obj(cls: Any, session: AsyncSession, id: int) -> str:
    # Check obj is exist or not
    obj = await get_obj(cls, session, id)
    if obj is None:
        return "Object not exist"
    query = delete(cls).where(cls.id == id)
    await session.execute(query)
    await session.commit()
    return "Deleted Successfully"

# Create vehicle in database check fleet_id is exist or not
async def create_vehicle_obj(
    session: AsyncSession, name: str, description: str, fleet_id: int
) -> Vehicle:
    query = select(Fleet).where(Fleet.id == fleet_id)
    results = await session.execute(query)
    temp = results.scalar()
    if temp is None:
        # raise Exception("Fleet not exist")
        return None
    vehicle : Vehicle = await create_obj(Vehicle, session, name=name, description = description, fleet_id=fleet_id)
    return vehicle

# Get all vehicle from database,
# if name is not None, get vehicle by name
# if fleet_id is not None, get vehicle by fleet_id
async def get_all_vehicles_obj(
    session: AsyncSession, name: str, fleet_id: int
) -> List[Vehicle]:
    query = select(Vehicle)
    if name:
        query = query.filter(Vehicle.name.like("%" + name + "%"))
    if fleet_id:
        query = query.filter(Vehicle.fleet_id == fleet_id)
    results = await session.execute(query)
    vehicle: List[Vehicle] = results.scalars().all()
    return vehicle

# Update vehicle in database
# check fleet_id is exist or not
async def update_vehicle_obj(
    session: AsyncSession, id: int, **kwargs: Any
) -> str:
    # Check fleet_id is exist or not
    fleet = await get_obj(Fleet, session, kwargs["fleet_id"])
    if fleet is None:
        return "Fleet not exist"
    # Update vehicle
    return await update_obj(Vehicle, session, id, **kwargs)

# Get route detail by route name
async def get_route_obj_by_name(
    session: AsyncSession,
    route_name: str,
    vehicle_name: str,
    driver_name: str,
) -> List[Route]:

    query = (
        select(Route)
        .join_from(
            Route,
            RouteDetail,
            RouteDetail.route_id == Route.id,
            isouter=True,
            full=True,
        )
        .join(Vehicle, RouteDetail.vehicle_id == Vehicle.id)
        .join(Driver, RouteDetail.driver_id == Driver.id)
    )

    if route_name:
        query = query.filter(Route.name.like("%" + route_name + "%"))
    if vehicle_name:
        query = query.filter(Vehicle.name.like("%" + vehicle_name + "%"))
    if driver_name:
        query = query.filter(Driver.name.like("%" + driver_name + "%"))

    results = await session.execute(query)
    route: List[Route] = results.scalars().all()
    return route

# Create route detail if route_id and vehicle_id and driver_id are exist
async def create_route_detail_obj(
    session: AsyncSession, **kwargs: Any
) -> RouteDetail:

    print("\n\n\n\n aaaa \n\n\n\n")
    # Check route_id, vehicle_id, driver_id is exist or not
    route = await get_obj(Route, session, kwargs["route_id"])
    vehicle = await get_obj(Vehicle, session, kwargs["vehicle_id"])
    driver = await get_obj(Driver, session, kwargs["driver_id"])
    if route is None or vehicle is None or driver is None:
        # raise Exception("Route, Vehicle or Driver not exist")
        return None
    
    print("\n\n\n\n hhhh \n\n\n\n")
    query = select(RouteDetail).where(
        RouteDetail.route_id == kwargs["route_id"],
        RouteDetail.vehicle_id == kwargs["vehicle_id"],
        RouteDetail.driver_id == kwargs["driver_id"]
    )
    results = await session.execute(query)
    temp = results.scalar()
    if temp is None:
        # kwargs["start_time"] = kwargs["start_time"].replace(tzinfo=datetime.utcnow().tzinfo)
        # kwargs["end_time"] = kwargs["end_time"].replace(tzinfo=datetime.utcnow().tzinfo)
        temp = await create_obj_db(RouteDetail, session, **kwargs)
    route_detail: RouteDetail = temp
    return route_detail

# Get route detail by route id and vehicle id
async def get_route_detail_obj(
    session: AsyncSession, route_id: int, vehicle_id: int
) -> Any:
    query = select(RouteDetail).where(
        RouteDetail.route_id == route_id, RouteDetail.vehicle_id == vehicle_id
    )
    results = await session.execute(query)
    route_detail = results.scalar()
    return route_detail

# Update route detail by route id and vehicle id
async def update_route_detail_obj(
    session: AsyncSession, route_id: int, vehicle_id: int, **kwargs: Any
) -> str:
    # Check obj is exist or not
    route_detail = await get_route_detail_obj(session, route_id, vehicle_id)
    if route_detail is None:
        return "Route Detail not exist"
    # Check driver_id is exist or not
    driver = await get_obj(Driver, session, kwargs["driver_id"])
    if driver is None:
        return "Driver not exist"
    query = (
        update(RouteDetail)
        .where(RouteDetail.route_id == route_id, RouteDetail.vehicle_id == vehicle_id)
        .values(**kwargs)
        .execution_options(synchronize_session="fetch")
    )

    await session.execute(query)
    await session.commit()
    return "Updated Successfully"

# Delete route detail by route id and vehicle id
async def delete_route_detail_obj(
    session: AsyncSession, route_id: int, vehicle_id: int
) -> str:
    # Check obj is exist or not
    route_detail = await get_route_detail_obj(session, route_id, vehicle_id)
    if route_detail is None:
        return "Route Detail not exist"
    query = delete(RouteDetail).where(
        RouteDetail.route_id == route_id, RouteDetail.vehicle_id == vehicle_id
    )
    await session.execute(query)
    await session.commit()
    return "Deleted Successfully"
