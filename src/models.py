from datetime import datetime
from typing import Any
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime,Date
from sqlalchemy.orm import declarative_base, relationship


Base: Any = declarative_base()


# Fleet model
class Fleet(Base):
    __tablename__ = "fleets"

    id = Column(Integer, primary_key=True, index = True)
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=True)
    vehicles : Any = relationship("Vehicle", cascade = "all,delete-orphan",back_populates="fleet")


# Vehicle model
class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index = True)
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=True)
    fleet_id = Column(Integer, ForeignKey("fleets.id"))
    fleet : Any = relationship("Fleet", back_populates="vehicles")
    route_details : Any = relationship("RouteDetail", cascade = "all,delete-orphan",back_populates="vehicle")

# Driver model
class Driver(Base):
    __tablename__ = "drivers"

    id = Column(Integer, primary_key=True, index = True)
    name = Column(String(255), nullable=False)
    age = Column(Date, nullable=False)
    route_details : Any = relationship("RouteDetail", cascade = "all,delete-orphan",back_populates="driver")

# Route model
class Route(Base):
    __tablename__ = "routes"

    id = Column(Integer, primary_key=True, index = True)
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=True)
    route_details : Any = relationship("RouteDetail", cascade = "all,delete-orphan",back_populates="route")
    

# Route Detail model
class RouteDetail(Base):
    __tablename__ = "route_details"

    route_id = Column(Integer, ForeignKey("routes.id"), primary_key=True, index = True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), primary_key=True, index = True)
    driver_id = Column(Integer, ForeignKey("drivers.id"),nullable=False)
    start_time = Column(DateTime, default=datetime.utcnow,  nullable=False)
    end_time = Column(DateTime, default=datetime.utcnow,  nullable=False)
    start_location = Column(String(255), nullable=False)
    end_location = Column(String(255), nullable=False)
    ticket_price = Column(Integer, nullable=False)
    route : Any = relationship("Route", back_populates="route_details")
    vehicle : Any = relationship("Vehicle", back_populates="route_details")
    driver : Any = relationship("Driver", back_populates="route_details")
