from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from . import schemas
from .controller import *
from .session import async_db_session as session
from .models import *

# Fleet endpoint
# -------------------------------------------------------------------------------------------------------------
api_fleet = APIRouter(prefix="/fleets",tags=["Fleet"])

# Create fleet
@api_fleet.post("/")
async def create_fleet(data: schemas.FleetCreate,session=Depends(session)):
    return await create_obj(Fleet,session,**data.dict())

# Get fleet
@api_fleet.get("/{id}", response_model=schemas.Fleet)
async def get_fleet(id: int = None,session=Depends(session)):
    return await get_obj(Fleet,session,id)

# Get all fleets
@api_fleet.get("/", response_model=List[schemas.Fleet])
async def get_fleets(name: str =None,session=Depends(session)):
    return await get_all_obj(Fleet,session,name)

# Update fleet
@api_fleet.put("/{id}")
async def update_fleet(id: int, data: schemas.FleetBase):
    return await update_obj(Fleet,session,id, **data.dict(),session=Depends(session))

# Delete fleet
@api_fleet.delete("/{id}")
async def delete_fleet(id: int,session=Depends(session)):
    return await delete_obj(Fleet,session,id)

# Vehicle endpoint
# -------------------------------------------------------------------------------------------------------------
api_vehicle = APIRouter(prefix="/vehicles",tags=["Vehicle"])

# Create vehicle
@api_vehicle.post("/")
async def create_vehicle(data: schemas.VehicleCreate,session=Depends(session)):
    return await create_obj(Vehicle, session,**data.dict())

# Get vehicle
@api_vehicle.get("/{id}", response_model=schemas.Vehicle)
async def get_vehicle(id: int = None,session=Depends(session)):
    return await get_obj(Vehicle, session,id)

# Get all vehicles
@api_vehicle.get("/", response_model=List[schemas.Vehicle])
async def get_vehicles(name: str = None,vehicle_id: int = None,session=Depends(session)):
    return await get_all_obj(Vehicle, session,name, vehicle_id)

# Update vehicle
@api_vehicle.put("/{id}")
async def update_vehicle(id:int,data: schemas.VehicleBase,session=Depends(session)):
    return await update_obj(Vehicle, session,id, **data.dict())

# Delete vehicle
@api_vehicle.delete("/")
async def delete_vehicles(id: int,session=Depends(session)):
    return await delete_obj(Vehicle, session,id)

# Driver endpoint
# -------------------------------------------------------------------------------------------------------------
api_driver = APIRouter(prefix="/drivers",tags=["Driver"])      
                          
@api_driver.post("/")
async def create_driver(data: schemas.DriverCreate,session=Depends(session)):
    return await create_obj(Driver, session, **data.dict())

# Get driver by id
async def get_driver(id:int = None,session=Depends(session)):
    return await get_obj(Driver, session, id)

# Get all drivers
@api_driver.get("/",response_model=List[schemas.Driver])
async def get_drivers(name: str= None,session=Depends(session)):
    return await get_all_obj(Driver, session, name)

# Update driver
@api_driver.put("/{id}")
async def update_driver(id:int, data: schemas.DriverBase,session=Depends(session)):
    return await update_obj(Driver, session, id,**data.dict())

# Delete driver
@api_driver.delete("/{id}")
async def delete_driver(id: int,session=Depends(session)):
    return await delete_obj(Driver, session, id)

# Route endpoint
# -------------------------------------------------------------------------------------------------------------
api_route = APIRouter(prefix="/routes",tags=["Route"])

# Create route
@api_route.post("/")
async def create_route(data: schemas.RouteCreate,session=Depends(session)):
    return await create_obj(Route, session, **data.dict())

# Get route
@api_route.get("/{id}", response_model = schemas.Route)
async def get_route(id:int=None,session=Depends(session)):
    return await get_obj(Route, session, id)

# Get all routes
@api_route.get("/", response_model = List[schemas.Route])
async def get_all_routes(route_name: str= None, vehicle_name: str= None,driver_name: str= None,session=Depends(session)):
    return await get_all_route(route_name, vehicle_name, driver_name)

# Update route
@api_route.put("/{id}")
async def update_route(id:int, data: schemas.RouteBase,session=Depends(session)):
    return await update_obj(Route, session, id,**data.dict())

# Delete route
@api_route.delete("/{id}")
async def delete_route(id:int,session=Depends(session)):
    return await delete_obj(Route, session, id)


# RouteDetail endpoint
# -------------------------------------------------------------------------------------------------------------
api_routedetail = APIRouter(prefix="/routedetails",tags=["Route Detail"])

# Create route
@api_routedetail.post("/")
async def create_route(data: schemas.RouteDetailCreate,session=Depends(session)):
    return await create_obj(RouteDetail, session, **data.dict())

# Get route detail
@api_routedetail.get("/{route_id}/{vehicle_id}", response_model = List[schemas.RouteDetail])
async def get_route_detail(route_id:int=None, vehicle_id:int=None,session=Depends(session)):
    route = await get_obj(RouteDetail, session, route_id, vehicle_id)
    print(route)
    return route

# Get all routes details
@api_routedetail.get("/",response_model = List[schemas.RouteDetail])
async def get_all_route_details(,session=Depends(session)):
    return await get_all_obj(RouteDetail, session, )

# Update route
@api_routedetail.put("/{route_id}/{vehicle_id}")
async def update_route(route_id:int,vehicle_id:int, data: schemas.RouteDetail,session=Depends(session)):
    return await update_obj(RouteDetail, session, route_id,vehicle_id,**data.dict())

# Delete route
@api_routedetail.delete("/{route_id}/{vehicle_id}")
async def delete_route(route_id: int, vehicle_id: int,session=Depends(session)):
    return await delete_obj(RouteDetail, session, route_id,vehicle_id)