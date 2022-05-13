import asyncio
from operator import mod
from pyexpat import model
from typing import List
from fastapi import FastAPI,APIRouter
from database import async_db_session

import schemas, models


# Fleet endpoint
# -------------------------------------------------------------------------------------------------------------
api_fleet = APIRouter(prefix="/fleets")

# Create fleet
@api_fleet.post("/")
async def create_fleet(data: schemas.FleetCreate):
    return await models.Fleet.create(**data.dict())

# Get fleet
@api_fleet.get("/", response_model=List[schemas.Fleet])
async def get_fleet(id: int = None ,name: str= None):
    return await models.Fleet.get(id,name)

# Get all fleets
@api_fleet.get("/", response_model=List[schemas.Fleet])
async def get_fleets():
    return await models.Fleet.get_all()

# Update fleet
@api_fleet.put("/{id}")
async def update_fleet(id: int, data: schemas.Fleet):
    return await models.Fleet.update(id, **data.dict())

# Delete fleet
@api_fleet.delete("/{id}")
async def delete_fleet(id: int):
    return await models.Fleet.delete(id)

# Vehicle endpoint
# -------------------------------------------------------------------------------------------------------------
api_vehicle = APIRouter(prefix="/vehicles")

# Create vehicle
@api_vehicle.post("/")
async def create_vehicle(data: schemas.VehicleCreate):
    return await models.Vehicle.create(**data.dict())

# Get vehicle
@api_vehicle.get("/{id}", response_model=List[schemas.Vehicle])
async def get_vehicle(id: int = None,name: str = None):
    return await models.Vehicle.get(id,name)

# Get all vehicles
@api_vehicle.get("/", response_model=List[schemas.Vehicle])
async def get_vehicles():
    return await models.Vehicle.get_all()

# Get vehicles by name
@api_vehicle.get("/{name}", response_model=List[schemas.Vehicle])
async def get_vehicles():
    return await models.Vehicle.get_by_name()

# Update vehicle
@api_vehicle.put("/{id}")
async def update_vehicle(data: schemas.Vehicle):
    return await models.Vehicle.update(id,data.dict())

# Delete vehicle
@api_vehicle.delete("/")
async def delete_vehicles(id: int):
    return await models.Vehicle.delete(id)

# Driver endpoint
# -------------------------------------------------------------------------------------------------------------
api_driver = APIRouter(prefix="/drivers")      
                          
@api_driver.post("/")
async def create_driver(data: schemas.DriverCreate):
    return await models.Driver.update(id,data.dict())

# Get driver by id
@api_driver.get("/",response_model=schemas.Driver)
async def get_driver(id:int = None,name:str=None):
    return await models.Driver.get(id,name)

# Get all drivers
@api_driver.get("/",response_model=List[schemas.Driver])
async def get_drivers():
    return await models.Driver.get_all()

# Update driver
@api_driver.put("/{id}")
async def update_driver(id:int, data: schemas.Driver):
    return await models.Driver.update(id,data.dict())

# Delete driver
@api_driver.delete("/{id}")
async def delete_driver(id: int):
    return await models.Driver.delete(id)

# Route endpoint
# -------------------------------------------------------------------------------------------------------------
api_route = APIRouter(prefix="/routes")

# Create route
@api_route.post("/")
async def create_route(id:int, data: schemas.RouteCreate):
    return await models.Route.create(id,data.dict())

# Get route
@api_route.get("/", response_model = List[schemas.Route])
async def get_route(id:int=None,name:str= None):
    return await models.Route.get(id,name)

# Get all routes
@api_route.get("/", response_model = List[schemas.Route])
async def get_all_routes():
    return await models.Route.get_all()

# Update route
@api_route.put("/{id}")
async def update_route(id:int, data: schemas.Route):
    return await models.Route.update(id,data.dict())

# Delete route
@api_route.delete("/{id}")
async def delete_route():
    return await models.Route.delete(id)

# Route Detail endpoint
# -------------------------------------------------------------------------------------------------------------
api_routedetail = APIRouter(prefix="/RouteDetail")

# Create route detail
@api_routedetail.post("/")
async def create_route_detail(data: schemas.RouteDetailCreate):
    return await models.RouteDetail.create(data)

# Get route detail
@api_routedetail.get("/",response_model= List[schemas.RouteDetail])
async def get_route_detail(route_id:int=None,vehicle_id:int =None,):
    return await models.get(route_id,vehicle_id)

# Get all routes detail
@api_routedetail.get("/all",response_model= List[schemas.RouteDetail])
async def get_all_route_detail():
    return await models.RouteDetail.get_all()

# Get all routes detail
@api_routedetail.get("/",response_model= List[schemas.RouteDetail])
async def get_all_route_detail():
    return await models.RouteDetail.get_all()

# Update route detail
@api_routedetail.put("/")
async def update_route_detail(route_id:int,vehicle_id:int,data:schemas.RouteDetail):
    return await models.RouteDetail.update_route_detail(route_id,vehicle_id,data)

# Delete route detail
@api_routedetail.delete("/")
async def delete_route_detail(route_id:int,vehicle_id:int):
    return await models.RouteDetail.delete_route_detail(route_id,vehicle_id)


    

"""
async def init_app():
    await async_db_session.init()
    await async_db_session.create_all()


async def create_user():
    await User.create(full_name="John Doe")
    user = await User.get(1)
    return user.id


async def create_post(user_id, data):
    await Post.create(user_id=user_id, data=data)
    posts = await Post.filter_by_user_id(user_id)
    return posts


async def update_user(id, full_name):
    await User.update(id, full_name="John Not Doe")
    user = await User.get(id)
    return user.full_name


async def async_main():
    await init_app()
    user_id = await create_user()
    await update_user(user_id, "John Not Doe")
    await create_post(user_id, "hello world")


asyncio.run(async_main())

"""