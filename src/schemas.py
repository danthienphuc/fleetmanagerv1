from re import A
from this import d
from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime, date


# Fleet schema
class FleetBase(BaseModel):
    name: str = Field(..., max_length=255, alias="Name", description="Name of fleet")
    description: str = Field(default=None, max_length=255, alias="Description")

    class Config:
        allow_population_by_field_name = True
        orm_mode = True


class FleetCreate(FleetBase):
    pass


class Fleet(FleetBase):
    id: int = Field(..., alias="ID", description="ID of Fleet")

    class Config:
        allow_population_by_field_name = True
        orm_mode = True


# Vehicle schema
class VehicleBase(BaseModel):
    name: str = Field(..., max_length=255, alias="Name")
    description: Optional[str] = Field(
        default=None, max_length=255, alias="Description"
    )
    fleet_id: int = Field(..., alias="FleetID")

    class Config:
        allow_population_by_field_name = True
        orm_mode = True


class VehicleCreate(VehicleBase):
    pass


class Vehicle(VehicleBase):
    id: int = Field(..., alias="ID", description="ID of Vehicle")

    class Config:
        allow_population_by_field_name = True
        orm_mode = True


# Driver schema
class DriverBase(BaseModel):
    name: str = Field(..., max_length=255, alias="Name")
    age: date = Field(..., alias="Age")

    class Config:
        allow_population_by_field_name = True
        orm_mode = True


class DriverCreate(DriverBase):
    pass


class Driver(DriverBase):
    id: int = Field(..., alias="ID", description="ID of Driver")

    class Config:
        allow_population_by_field_name = True
        orm_mode = True


# Route schema
class RouteBase(BaseModel):
    name: str = Field(..., max_length=255, alias="Name")
    description: Optional[str] = Field(
        default=None, max_length=255, alias="Description"
    )

    class Config:
        allow_population_by_field_name = True
        orm_mode = True


class RouteCreate(RouteBase):
    pass


class Route(RouteBase):
    id: int = Field(..., alias="ID", description="ID of Route")

    class Config:
        allow_population_by_field_name = True
        orm_mode = True


# Route Detail schema
class RouteDetailBase(BaseModel):
    driver_id: int = Field(..., alias="DriverID")
    start_time: datetime = Field(..., alias="StartTime")
    end_time: datetime = Field(..., alias="EndTime")
    start_location: str = Field(..., max_length=255, alias="StartLocation")
    end_location: str = Field(..., max_length=255, alias="EndLocation")
    ticket_price: int = Field(..., alias="TicketPrice")

    class Config:
        allow_population_by_field_name = True
        orm_mode = True


class RouteDetailCreate(RouteDetailBase):
    route_id: int = Field(
        ..., alias="RouteID", description="RouteID index of Route Detail"
    )
    vehicle_id: int = Field(
        ..., alias="VehicleID", description="VehicleID index of Route Detail"
    )

    class Config:
        allow_population_by_field_name = True
        orm_mode = True


class RouteDetail(RouteDetailCreate):
    pass

    class Config:
        orm_mode = True
