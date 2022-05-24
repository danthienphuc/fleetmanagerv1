from ntpath import join
from xmlrpc.client import DateTime
from sqlalchemy import Column, ForeignKey, Integer, String, Date,Time
from sqlalchemy import update,delete
from sqlalchemy.future import select
from sqlalchemy.orm import relationship

from .database import Base, async_db_session


class BatchModel:
    @classmethod
    async def create(cls, **kwargs):
        async_db_session.add(cls(**kwargs))
        await async_db_session.commit()
        return "Created Successfully"

    @classmethod
    async def get(cls, id = None,*args,**kwargs):
        query = select(cls).where(cls.id == id)
        results = await async_db_session.execute(query)
        return results.scalar()
    
    @classmethod
    async def get_all(cls,name = None,*args,**kwargs):
        if name is None:
            query = select(cls)
        else:
            query = select(cls).where(cls.name == name)
        results = await async_db_session.execute(query)
        return results.scalars().all()
    
    @classmethod
    async def update(cls, id,*args,**kwargs):
        query = (
            update(cls)
            .where(cls.id == id)
            .values(**kwargs)
            .execution_options(synchronize_session="fetch")
        )

        await async_db_session.execute(query)
        await async_db_session.commit()
        return "Updated Successfully"


    @classmethod
    async def delete(cls, id,*args,**kwargs):
        query = (
            delete(cls).where(cls.id == id)
        )
        await async_db_session.excute(query)
        await async_db_session.commit()
        return "Deleted Successfully"


# Fleet model
class Fleet(Base,BatchModel):
    __tablename__ = "fleets"

    id = Column(Integer, primary_key=True, index = True)
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)


# Vehicle model
class Vehicle(Base,BatchModel):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index = True)
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    fleet_id = Column(Integer, ForeignKey("fleets.id"), nullable=False)
    
    @classmethod
    async def get_all(cls,name = None,vehicle_id = None,*args,**kwargs):
        query = select(cls)
        if name is not None:
            query.filter(cls.name == name)
        if vehicle_id is not None:
            query.filter(cls.id == vehicle_id)

        results = await async_db_session.execute(query)
        return results.scalars().all()

# Driver model
class Driver(Base,BatchModel):
    __tablename__ = "drivers"

    id = Column(Integer, primary_key=True, index = True)
    name = Column(String(255), nullable=False)
    age = Column(Date, nullable=False)

# Route model
class Route(Base,BatchModel):
    __tablename__ = "routes"

    id = Column(Integer, primary_key=True, index = True)
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    
    @classmethod
    async def get_all(cls,name = None,*args,**kwargs):
        query = select(cls)
        if name is not None:
            query.filter(cls.name == name)
        results = await async_db_session.execute(query)
        return results.scalars().all()

# Route Detail model
class RouteDetail(Base,BatchModel):
    __tablename__ = "route_details"

    route_id = Column(Integer, ForeignKey("routes.id"), primary_key=True, index = True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), primary_key=True, index = True)
    driver_id = Column(Integer, ForeignKey("drivers.id"), index = True)
    start_time = Column(Date)
    end_time = Column(Date)
    start_location = Column(String(255), nullable=False)
    end_location = Column(String(255), nullable=False)
    ticket_price = Column(Integer, nullable=False)

    @classmethod
    async def get(cls,route_id,vehicle_id,*args,**kwargs):
        query = select(cls).where(cls.route_id == route_id).where(cls.vehicle_id == vehicle_id)
        results = await async_db_session.execute(query)
        return results.scalar()
    
    @classmethod
    async def get_all_route(cls,route_name = None,vehicle_name = None, driver_name =None,*args,**kwargs):
        query = select(Route).\
            select_from(RouteDetail.join(Route).join(Vehicle).join(Driver)).\
            where(
            Route.name == route_name,
            Vehicle.name == vehicle_name,
            Driver.name == driver_name)
        if(route_name):
            query.filter(Route.name == route_name)
        if(vehicle_name):
            query.filter(Vehicle.name == vehicle_name)
        if(driver_name):
            query.filter(Driver.name == driver_name)
        
        results = await async_db_session.execute(query)
        return results.scalars().all()
    
    @classmethod
    async def update(cls, route_id,vehicle_id,*args,**kwargs):
        query = (
            update(cls)
            .where(cls.route_id == route_id, cls.vehicle_id == vehicle_id)
            .values(**kwargs)
            .execution_options(synchronize_session="fetch")
        )

        await async_db_session.execute(query)
        await async_db_session.commit()
        return "Updated Successfully"

    @classmethod
    async def delete(cls, route_id,vehicle_id,*args,**kwargs):
        query = (
            delete(cls).where(cls.route_id == route_id, cls.vehicle_id == vehicle_id)
        )
        await async_db_session.excute(query)
        await async_db_session.commit()
        return "Deleted Successfully"