from typing import List
from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from . import schemas, models


# Fleet endpoint
# -------------------------------------------------------------------------------------------------------------
api_fleet = APIRouter(prefix="/fleets",tags=["Fleet"])

# Create fleet
@api_fleet.post("/")
async def create_fleet(data: schemas.FleetCreate):
    return await models.Fleet.create(**data.dict())

# Get fleet
@api_fleet.get("/{id}", response_model=schemas.Fleet)
async def get_fleet(id: int = None):
    return await models.Fleet.get(id)

# Get all fleets
@api_fleet.get("/", response_model=List[schemas.Fleet])
async def get_fleets(name: str =None):
    return await models.Fleet.get_all(name)

# Update fleet
@api_fleet.put("/{id}")
async def update_fleet(id: int, data: schemas.FleetBase):
    return await models.Fleet.update(id, **data.dict())

# Delete fleet
@api_fleet.delete("/{id}")
async def delete_fleet(id: int):
    return await models.Fleet.delete(id)

# Vehicle endpoint
# -------------------------------------------------------------------------------------------------------------
api_vehicle = APIRouter(prefix="/vehicles",tags=["Vehicle"])

# Create vehicle
@api_vehicle.post("/")
async def create_vehicle(data: schemas.VehicleCreate):
    return await models.Vehicle.create(**data.dict())

# Get vehicle
@api_vehicle.get("/{id}", response_model=schemas.Vehicle)
async def get_vehicle(id: int = None):
    return await models.Vehicle.get(id)

# Get all vehicles
@api_vehicle.get("/", response_model=List[schemas.Vehicle])
async def get_vehicles(name: str = None,vehicle_id: int = None):
    return await models.Vehicle.get_all(name, vehicle_id)

# Update vehicle
@api_vehicle.put("/{id}")
async def update_vehicle(id:int,data: schemas.VehicleBase):
    return await models.Vehicle.update(id, **data.dict())

# Delete vehicle
@api_vehicle.delete("/")
async def delete_vehicles(id: int):
    return await models.Vehicle.delete(id)

# Driver endpoint
# -------------------------------------------------------------------------------------------------------------
api_driver = APIRouter(prefix="/drivers",tags=["Driver"])      
                          
@api_driver.post("/")
async def create_driver(data: schemas.DriverCreate):
    return await models.Driver.create(**data.dict())

# Get driver by id
@api_driver.get("/{id}",response_model=schemas.Driver)
async def get_driver(id:int = None):
    return await models.Driver.get(id)

# Get all drivers
@api_driver.get("/",response_model=List[schemas.Driver])
async def get_drivers(name: str= None):
    return await models.Driver.get_all(name)

# Update driver
@api_driver.put("/{id}")
async def update_driver(id:int, data: schemas.DriverBase):
    return await models.Driver.update(id,**data.dict())

# Delete driver
@api_driver.delete("/{id}")
async def delete_driver(id: int):
    return await models.Driver.delete(id)

# Route endpoint
# -------------------------------------------------------------------------------------------------------------
api_route = APIRouter(prefix="/routes",tags=["Route"])

# Create route
@api_route.post("/")
async def create_route(data: schemas.RouteCreate):
    return await models.Route.create(**data.dict())

# Get route
@api_route.get("/{id}", response_model = schemas.Route)
async def get_route(id:int=None):
    return await models.Route.get(id)

# Get all routes
@api_route.get("/", response_model = List[schemas.Route])
async def get_all_routes(route_name: str= None, vehicle_name: str= None,driver_name: str= None):
    return await models.RouteDetail.get_all_route(route_name, vehicle_name, driver_name)

# Update route
@api_route.put("/{id}")
async def update_route(id:int, data: schemas.RouteBase):
    return await models.Route.update(id,**data.dict())

# Delete route
@api_route.delete("/{id}")
async def delete_route():
    return await models.Route.delete(id)


# RouteDetail endpoint
# -------------------------------------------------------------------------------------------------------------
api_routedetail = APIRouter(prefix="/routedetails",tags=["Route Detail"])

# Create route
@api_routedetail.post("/")
async def create_route(data: schemas.RouteDetailCreate):
    return await models.RouteDetail.create(**data.dict())

# Get route detail
@api_routedetail.get("/{route_id}/{vehicle_id}", response_model = List[schemas.RouteDetail])
async def get_route_detail(route_id:int=None, vehicle_id:int=None):
    route = await models.RouteDetail.get(route_id, vehicle_id)
    print(route)
    return route


# Get all routes details
@api_routedetail.get("/",response_model = List[schemas.RouteDetail])
async def get_all_route_details():
    return await models.RouteDetail.get_all()

# Update route
@api_routedetail.put("/{route_id}/{vehicle_id}")
async def update_route(route_id:int,vehicle_id:int, data: schemas.RouteDetail):
    return await models.RouteDetail.update(route_id,vehicle_id,**data.dict())

# Delete route
@api_routedetail.delete("/{route_id}/{vehicle_id}")
async def delete_route(route_id: int, vehicle_id: int):
    return await models.RouteDetail.delete(route_id,vehicle_id)