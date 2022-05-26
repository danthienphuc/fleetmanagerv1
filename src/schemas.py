from typing import Optional
from pydantic import BaseModel
from datetime import date


# Fleet schema
class FleetBase(BaseModel):
    name: str
    description: str

class FleetCreate(FleetBase):
    pass

class Fleet(FleetBase):
    id: int
    

    class Config:
        orm_mode = True

# Vehicle schema
class VehicleBase(BaseModel):
    name: str
    description: str
    fleet_id: int

class VehicleCreate(VehicleBase):
    pass

class Vehicle(VehicleBase):
    id: int

    class Config:
        orm_mode = True

# Driver schema
class DriverBase(BaseModel):
    name: str
    age: date

class DriverCreate(DriverBase):
    pass

class Driver(DriverBase):
    id: int

    class Config:
        orm_mode = True

# Route schema
class RouteBase(BaseModel):
    name: str
    description: str


class RouteCreate(RouteBase):
    pass

class Route(RouteBase):
    id: int

    class Config:
        orm_mode = True

# Route Detail schema
class RouteDetailBase(BaseModel):
    driver_id: int
    start_time: Optional[date] = None
    end_time: Optional[date] = None
    start_location: str
    end_location: str
    ticket_price: int


class RouteDetailCreate(RouteDetailBase):
    route_id: int
    vehicle_id: int

class RouteDetail(RouteDetailCreate):
    pass

    class Config:
        orm_mode = True