from sqlalchemy import Column, ForeignKey, Integer, String, Date, join
from sqlalchemy import update,delete
from sqlalchemy.future import select

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
            query = select(cls).where(cls.name.like("%"+name+"%"))
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
        await async_db_session.execute(query)
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
    async def get_all(cls,name = None,fleet_id = None,*args,**kwargs):
        query = select(cls)
        if name:
            query = query.filter(cls.name.like("%"+name+"%"))
        if fleet_id:
            query = query.filter(cls.fleet_id == fleet_id)
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
    async def get(cls,route_id,vehicle_id):
        query = select(cls).where(cls.route_id == route_id,cls.vehicle_id == vehicle_id)
        results = await async_db_session.execute(query)
        return results.scalars().all()
    
    @classmethod
    async def get_all_route(cls,route_name = None,vehicle_name = None, driver_name =None,*args,**kwargs):
        
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
        await async_db_session.execute(query)
        await async_db_session.commit()
        return "Deleted Successfully"