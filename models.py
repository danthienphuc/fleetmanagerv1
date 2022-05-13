from operator import index
from sqlalchemy import Column, ForeignKey, Integer, String, Date,Time
from sqlalchemy import update,delete
from sqlalchemy.future import select
from sqlalchemy.orm import relationship

from database import Base, async_db_session


class BatchModel(Base):

    @classmethod
    async def create(cls, **kwargs):
        async_db_session.add(cls(**kwargs))
        await async_db_session.commit()
        return "Create Successful"

    @classmethod
    async def get(cls, id):
        query = select(cls).where(cls.id == id)
        results = await async_db_session.execute(query)
        (result,) = results.one()
        return result
    
    @classmethod
    async def get_all(cls):
        query = select(cls)
        results = await async_db_session.execute(query)
        return results.fetchall()

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
class Fleet(BatchModel):
    __tablename__ = "fleets"

    id = Column(Integer, primary_key=True, index = True)
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)

    vehicles = relationship("Vehicles", backref="fleets")


# Vehicle model
class Vehicle(BatchModel):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index = True)
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    fleet_id = Column(Integer, ForeignKey("fleets.id"), nullable=False)

# Driver model
class Driver(BatchModel):
    __tablename__ = "drivers"

    id = Column(Integer, primary_key=True, index = True)
    name = Column(String(255), nullable=False)
    age = Column(Date, nullable=False)

# Route model
class Route(BatchModel):
    __tablename__ = "routes"

    id = Column(Integer, primary_key=True, index = True)
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)

# Route Detail model
class RouteDetail(BatchModel):
    __tablename__ = "route_details"

    route_id = Column(Integer, ForeignKey("routes.id"), primary_key=True, index = True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), primary_key=True, index = True)
    driver_id = Column(Integer, ForeignKey("drivers.id"), index = True)
    start_date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)

"""

# User model
class User(Base, ModelAdmin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String)
    posts = relationship("Post")

    # required in order to acess columns with server defaults
    # or SQL expression defaults, subsequent to a flush, without
    # triggering an expired load
    __mapper_args__ = {"eager_defaults": True}

    def __repr__(self):
        return (
            f"<{self.__class__.__name__}("
            f"id={self.id}, "
            f"full_name={self.full_name}, "
            f"posts={self.posts}, "
            f")>"
        )


class Post(Base, ModelAdmin):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(ForeignKey("users.id"))
    data = Column(String)

    def __repr__(self):
        return (
            f"<{self.__class__.__name__}(" f"id={self.id}, " f"data={self.data}" f")>"
        )

    @classmethod
    async def filter_by_user_id(cls, user_id):
        query = select(cls).where(cls.user_id == user_id)
        posts = await async_db_session.execute(query)
        return posts.scalars().all()
"""