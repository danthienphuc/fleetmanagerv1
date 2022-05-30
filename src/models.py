from pydantic import BaseModel
from sqlalchemy import Column, ForeignKey, Integer, String, Date
from sqlalchemy.orm import declarative_base

BaseModel = declarative_base()


# Fleet model
class Fleet(BaseModel):
    __tablename__ = "fleets"

    id = Column(Integer, primary_key=True, index = True)
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)


# Vehicle model
class Vehicle(BaseModel):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index = True)
    name = Column(String(255))
    description = Column(String(255))
    fleet_id = Column(Integer, ForeignKey("fleets.id"), nullable=False)

# Driver model
class Driver(BaseModel):
    __tablename__ = "drivers"

    id = Column(Integer, primary_key=True, index = True)
    name = Column(String(255), nullable=False)
    age = Column(Date, nullable=False)

# Route model
class Route(BaseModel):
    __tablename__ = "routes"

    id = Column(Integer, primary_key=True, index = True)
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    

# Route Detail model
class RouteDetail(BaseModel):
    __tablename__ = "route_details"

    route_id = Column(Integer, ForeignKey("routes.id"), primary_key=True, index = True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), primary_key=True, index = True)
    driver_id = Column(Integer, ForeignKey("drivers.id"), index = True)
    start_time = Column(Date)
    end_time = Column(Date)
    start_location = Column(String(255), nullable=False)
    end_location = Column(String(255), nullable=False)
    ticket_price = Column(Integer, nullable=False)