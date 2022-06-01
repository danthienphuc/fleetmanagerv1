from sqlalchemy import Column, ForeignKey, Integer, String, DateTime,Date
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


# Fleet model
class Fleet(Base):
    __tablename__ = "fleets"

    id = Column(Integer, primary_key=True, index = True)
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    vehicles = relationship("Vehicle", cascade = "all,delete-orphan",backref="vehicles")


# Vehicle model
class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index = True)
    name = Column(String(255))
    description = Column(String(255))
    fleet_id = Column(Integer, ForeignKey("fleets.id"))

# Driver model
class Driver(Base):
    __tablename__ = "drivers"

    id = Column(Integer, primary_key=True, index = True)
    name = Column(String(255), nullable=False)
    age = Column(Date, nullable=False)

# Route model
class Route(Base):
    __tablename__ = "routes"

    id = Column(Integer, primary_key=True, index = True)
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    

# Route Detail model
class RouteDetail(Base):
    __tablename__ = "route_details"

    route_id = Column(Integer, ForeignKey("routes.id"), primary_key=True, index = True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), primary_key=True, index = True)
    driver_id = Column(Integer, ForeignKey("drivers.id"), index = True)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    start_location = Column(String(255), nullable=False)
    end_location = Column(String(255), nullable=False)
    ticket_price = Column(Integer, nullable=False)