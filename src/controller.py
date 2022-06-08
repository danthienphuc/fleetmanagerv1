from typing import List, Optional
from sqlalchemy import join, update,delete
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from .models import *


async def create_obj(cls:type,session:AsyncSession, **kwargs:Any)->Any:
    obj = cls(**kwargs)
    session.add(obj)
    await session.commit()
    await session.refresh(obj)
    return obj

async def get_obj(cls:type,session:AsyncSession, id:int)->Any:
    query = select(cls).where(cls.id == id)
    results = await session.execute(query)
    return results.scalar()

async def get_all_obj(cls:type,session:AsyncSession,name:Optional[str] = None)->Any:
    if name is None:
        query = select(cls)
    else:
        query = select(cls).where(cls.name.like("%"+name+"%"))
    results = await session.execute(query)
    return results.scalars().all()

async def update_obj(cls:type,session:AsyncSession, id:int,**kwargs:Any)->str:
    query = (
        update(cls)
        .where(cls.id == id)
        .values(**kwargs)
        .execution_options(synchronize_session="fetch")
    )

    await session.execute(query)
    await session.commit()
    return "Updated Successfully"

async def delete_obj(cls:type,session:AsyncSession, id:int)->str:
    query = (
        delete(cls).where(cls.id == id)
    )
    await session.execute(query)
    await session.commit()
    return "Deleted Successfully"



async def get_all_vehicles_obj(session:AsyncSession,name:Optional[str] = None,fleet_id: Optional[int]= None)->Any:
    query = select(Vehicle)
    if name:
        query = query.filter(Vehicle.name.like("%"+name+"%"))
    if fleet_id:
        query = query.filter(Vehicle.fleet_id == fleet_id)
    results = await session.execute(query)
    return results.scalars().all()

async def get_route_detail_obj(session:AsyncSession,route_id:int,vehicle_id:int)->Any:
    query = select(RouteDetail).where(RouteDetail.route_id == route_id,RouteDetail.vehicle_id == vehicle_id)
    results = await session.execute(query)
    return results.scalar()

async def get_all_route_obj(session:AsyncSession,route_name:Optional[str] = None,vehicle_name:Optional[str] = None, driver_name:Optional[str] =None)->Any:
    query = select(Route).\
        select_from(join(Route,RouteDetail,RouteDetail.route_id==Route.id, isouter=True,full = True).\
            join(Vehicle,RouteDetail.vehicle_id==Vehicle.id).\
                join(Driver,RouteDetail.driver_id == Driver.id))
    if(route_name):
        query = query.filter(Route.name.like("%"+route_name+"%"))
    if(vehicle_name):
        query = query.filter(Vehicle.name.like("%"+vehicle_name+"%"))
    if(driver_name):
        query = query.filter(Driver.name.like("%"+driver_name+"%"))
    
    results = await session.execute(query)
    return results.scalars().all()

async def update_route_detail_obj(session:AsyncSession, route_id:int,vehicle_id:int,**kwargs:Any)->str:
    query = (
        update(RouteDetail)
        .where(RouteDetail.route_id == route_id, RouteDetail.vehicle_id == vehicle_id)
        .values(**kwargs)
        .execution_options(synchronize_session="fetch")
    )

    await session.execute(query)
    await session.commit()
    return "Updated Successfully"

async def delete_route_detail_obj(session:AsyncSession,route_id:int,vehicle_id:int)->str:
    query = (
        delete(RouteDetail).where(RouteDetail.route_id == route_id, RouteDetail.vehicle_id == vehicle_id)
    )
    await session.execute(query)
    await session.commit()
    return "Deleted Successfully"