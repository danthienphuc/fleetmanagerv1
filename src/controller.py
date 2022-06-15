from typing import List
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
    query = delete(cls).where(cls.id == id)
    await session.execute(query)
    await session.commit()
    return "Deleted Successfully"

# Create vehicle in database check fleet_id is exist or not
async def create_vehicle_obj(
    session: AsyncSession, name: str, description: str, fleet_id: int
) -> Vehicle:
    query = select(Vehicle).where(Vehicle.fleet_id == fleet_id)
    results = await session.execute(query)
    temp = results.scalar()
    if temp is None:
        temp = await create_obj(Vehicle, session, name=name, description = description, fleet_id=fleet_id)
    print(temp.id)
    vehicle : Vehicle = temp
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
    query = delete(RouteDetail).where(
        RouteDetail.route_id == route_id, RouteDetail.vehicle_id == vehicle_id
    )
    await session.execute(query)
    await session.commit()
    return "Deleted Successfully"
