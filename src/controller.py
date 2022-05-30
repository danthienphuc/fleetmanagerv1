from typing import Generator
from sqlalchemy import Column, ForeignKey, Integer, String, Date, join, update,delete
from sqlalchemy.future import select
from .old.models import Route,Vehicle,Driver,RouteDetail


async def create_obj(cls,session, **kwargs):
    session.add(cls(**kwargs))
    await session.commit()
    return "Created Successfully"

async def get_obj(cls,session, id = None):
    query = select(cls).where(cls.id == id)
    results = await session.execute(query)
    return results.scalar()

async def get_all_obj(cls,session,name = None):
    if name is None:
        query = select(cls)
    else:
        query = select(cls).where(cls.name.like("%"+name+"%"))
    results = await session.execute(query)
    return results.scalars().all()

async def update_obj(cls,session, id,**kwargs):
    query = (
        update(cls)
        .where(cls.id == id)
        .values(**kwargs)
        .execution_options(synchronize_session="fetch")
    )

    await session.execute(query)
    await session.commit()
    return "Updated Successfully"

async def delete_obj(cls,session, id):
    query = (
        delete(cls).where(cls.id == id)
    )
    await session.execute(query)
    await session.commit()
    return "Deleted Successfully"



async def get_all_fleet(cls,session,name = None,fleet_id = None,*args,**kwargs):
    query = select(cls)
    if name:
        query = query.filter(cls.name.like("%"+name+"%"))
    if fleet_id:
        query = query.filter(cls.fleet_id == fleet_id)
    results = await session.execute(query)
    return results.scalars().all()

async def get_fleet(cls,session,route_id,vehicle_id):
    query = select(cls).where(cls.route_id == route_id,cls.vehicle_id == vehicle_id)
    results = await session.execute(query)
    return results.scalars().all()

async def get_all_route(cls,session,route_name = None,vehicle_name = None, driver_name =None,*args,**kwargs):
    query = select(Route).\
        select_from(join(cls, Route,cls.route_id==Route.id).\
            join(Vehicle,cls.vehicle_id==Vehicle.id).\
                join(Driver,cls.driver_id == Driver.id))
    if(route_name):
        query = query.filter(Route.name.like("%"+route_name+"%"))
    if(vehicle_name):
        query = query.filter(Vehicle.name.like("%"+vehicle_name+"%"))
    if(driver_name):
        query = query.filter(Driver.name.like("%"+driver_name+"%"))
    
    results = await session.execute(query)
    return results.scalars().all()

async def update_route_detail(cls,session, route_id,vehicle_id,*args,**kwargs):
    query = (
        update(cls)
        .where(cls.route_id == route_id, cls.vehicle_id == vehicle_id)
        .values(**kwargs)
        .execution_options(synchronize_session="fetch")
    )

    await session.execute(query)
    await session.commit()
    return "Updated Successfully"

async def delete_route_detail(cls,session, route_id,vehicle_id,*args,**kwargs):
    query = (
        delete(cls).where(cls.route_id == route_id, cls.vehicle_id == vehicle_id)
    )
    await session.execute(query)
    await session.commit()
    return "Deleted Successfully"