from lib2to3.pgen2.token import OP
from typing import List, Union
from fastapi import Query
from sqlalchemy import join, update, delete
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from .models import *


async def create_obj(cls: Any, session: AsyncSession, **kwargs: Any) -> Any:
    obj = cls(**kwargs)
    session.add(obj)
    await session.commit()
    await session.refresh(obj)
    return obj


async def get_obj(cls: Any, session: AsyncSession, id: int) -> Any:
    query = select(cls).where(cls.id == id)
    results = await session.execute(query)
    return results.scalar()


async def get_all_obj(cls: Any, session: AsyncSession, name: str = Query(None)) -> Any:
    query = select(cls)
    if name is not None:
        query = query.filter(cls.name.like("%" + name + "%"))
    results = await session.execute(query)
    return results.scalars().all()


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


async def delete_obj(cls: Any, session: AsyncSession, id: int) -> str:
    query = delete(cls).where(cls.id == id)
    await session.execute(query)
    await session.commit()
    return "Deleted Successfully"


async def get_all_vehicles_obj(
    session: AsyncSession, name: str, fleet_id: int
) -> List[Vehicle]:
    query = select(Vehicle)
    if name:
        query = query.filter(Vehicle.name.like("%" + name + "%"))  # type: ignore
    if fleet_id:
        query = query.filter(Vehicle.fleet_id == fleet_id)
    results = await session.execute(query)
    vehicle: List[Vehicle] = results.scalars().all()
    return vehicle


async def get_all_route_obj(
    session: AsyncSession,
    route_name: str,
    vehicle_name: str,
    driver_name: str,
) -> List[Route]:
    query = select(Route).select_from(
        join(
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
        query = query.filter(Route.name.like("%" + route_name + "%"))  # type: ignore
    if vehicle_name:
        query = query.filter(Vehicle.name.like("%" + vehicle_name + "%"))  # type: ignore
    if driver_name:
        query = query.filter(Driver.name.like("%" + driver_name + "%"))  # type: ignore

    results = await session.execute(query)
    route: List[Route] = results.scalars().all()
    return route

async def get_all_route_detail_obj(session: AsyncSession, name: str = Query(None)) -> Any:
    results = await session.execute(select(RouteDetail))
    return results.scalars().all()

async def get_route_detail_obj(
    session: AsyncSession, route_id: int, vehicle_id: int
) -> RouteDetail:
    query = select(RouteDetail).where(
        RouteDetail.route_id == route_id, RouteDetail.vehicle_id == vehicle_id
    )
    results = await session.execute(query)
    route_detail: RouteDetail = results.scalar()
    return route_detail

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


async def delete_route_detail_obj(
    session: AsyncSession, route_id: int, vehicle_id: int
) -> str:
    query = delete(RouteDetail).where(
        RouteDetail.route_id == route_id, RouteDetail.vehicle_id == vehicle_id
    )
    await session.execute(query)
    await session.commit()
    return "Deleted Successfully"
