from datetime import date, datetime
from typing import Any
from pyparsing import Optional
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Date
from sqlalchemy.orm import declarative_base, relationship


Base: Any = declarative_base()


# Fleet model
class Fleet(
    Base,
):
    __tablename__ = "fleets"

    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String(255), nullable=False)
    description: str = Column(String(255), nullable=True)
    vehicles: "Vehicle" = relationship(
        "Vehicle", cascade="all,delete-orphan", back_populates="fleet"
    )


# Vehicle model
class Vehicle(Base):
    __tablename__ = "vehicles"

    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String(255), nullable=False)
    description: str = Column(String(255), nullable=True)
    fleet_id: int = Column(Integer, ForeignKey("fleets.id"))
    fleet: Fleet = relationship("Fleet", back_populates="vehicles")
    route_details: "RouteDetail" = relationship(
        "RouteDetail", cascade="all,delete-orphan", back_populates="vehicle"
    )


# Driver model
class Driver(Base):
    __tablename__ = "drivers"

    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String(255), nullable=False)
    age: date = Column(Date, nullable=False)
    route_details: "RouteDetail" = relationship(
        "RouteDetail", cascade="all,delete-orphan", back_populates="driver"
    )


# Route model
class Route(Base):
    __tablename__ = "routes"

    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String(255), nullable=False)
    description: str = Column(String(255), nullable=True)
    route_details: "RouteDetail" = relationship(
        "RouteDetail", cascade="all,delete-orphan", back_populates="route"
    )


# Route Detail model
class RouteDetail(Base):
    __tablename__ = "route_details"

    route_id: int = Column(
        Integer, ForeignKey("routes.id"), primary_key=True, index=True
    )
    vehicle_id: int = Column(
        Integer, ForeignKey("vehicles.id"), primary_key=True, index=True
    )
    driver_id: int = Column(Integer, ForeignKey("drivers.id"), nullable=False)
    start_time: datetime = Column(DateTime, default=datetime.utcnow, nullable=False)
    end_time: datetime = Column(DateTime, default=datetime.utcnow, nullable=False)
    start_location: str = Column(String(255), nullable=False)
    end_location: str = Column(String(255), nullable=False)
    ticket_price: int = Column(Integer, nullable=False)
    route: Route = relationship("Route", back_populates="route_details")
    vehicle: Vehicle = relationship("Vehicle", back_populates="route_details")
    driver: Driver = relationship("Driver", back_populates="route_details")
