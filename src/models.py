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
        return "Create Successful"

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
    async def update(cls, id, **kwargs):
        query = (
            update(cls)
            .where(cls.id == id)
            .values(**kwargs)
            .execution_options(synchronize_session="fetch")
        )

        await async_db_session.execute(query)
        await async_db_session.commit()
        return "Update Successful!"


    @classmethod
    async def delete(cls, id):
        query = (
            delete(cls).where(cls.id == id)
        )
        await async_db_session.excute(query)
        await async_db_session.commit()
        return "Delete Successful"


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
        if name is None or vehicle_id is None:
            query = select(cls)
        else:
            query = select(cls).where(cls.name == name,cls.vehicle_id == vehicle_id)
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
        if name is None:
            query = select(cls)
        else:
            query = select(cls).where(cls.name == name)
        results = await async_db_session.execute(query)
        return results.scalars().all()

# Route Detail model
class RouteDetail(Base,BatchModel):
    __tablename__ = "route_details"

    route_id = Column(Integer, ForeignKey("routes.id"), primary_key=True, index = True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), primary_key=True, index = True)
    driver_id = Column(Integer, ForeignKey("drivers.id"), index = True)
    start_date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    
    @classmethod
    async def get_all_route(cls,route_name = None,vehicle_name = None, driver_name =None,*args,**kwargs):
        if route_name & vehicle_name & driver_name:
            query = select(Route)
        else:
            query = select([Route]).selectfrom(cls,Route,Vehicle,Driver).where(
                cls.route_id == Route.id,
                cls.driver_id == Driver.id,
                cls.vehicle_id == Vehicle.id,
                Route.name == route_name,
                Driver.name == driver_name,
                Vehicle.name == vehicle_name
                )
        results = await async_db_session.execute(query)
        return results.scalars().all()