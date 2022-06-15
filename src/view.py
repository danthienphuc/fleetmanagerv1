import logging
from typing import List
from fastapi import APIRouter, Depends, Query
from . import schemas
from .controller import *
from .session import async_db_session as session
from .models import *


# Fleet endpoint
# -------------------------------------------------------------------------------------------------------------
api_fleet = APIRouter(prefix="/fleets", tags=["Fleet"])

# Create fleet
@api_fleet.post("/", response_model=schemas.Fleet)
async def create_fleet(
    data: schemas.FleetCreate, session: AsyncSession = Depends(session)
) -> Fleet:
    fleet: Fleet = await create_obj(Fleet, session, **data.dict())
    return fleet


# Get fleet
@api_fleet.get("/{id}", response_model=schemas.Fleet)
async def get_fleet(id: int, session: AsyncSession = Depends(session)) -> Fleet:
    fleet: Fleet = await get_obj(Fleet, session, id)
    return fleet


# Get all fleets
@api_fleet.get("/", response_model=List[schemas.Fleet])
async def get_fleets(
    name: str = Query(None), session: AsyncSession = Depends(session)
) -> List[Fleet]:
    fleet: List[Fleet] = await get_all_obj(Fleet, session, name)
    return fleet


# Update fleet
@api_fleet.put("/{id}")
async def update_fleet(
    id: int, data: schemas.FleetBase, session: AsyncSession = Depends(session)
) -> str:
    return await update_obj(Fleet, session, id, **data.dict())


# Delete fleet
@api_fleet.delete("/{id}")
async def delete_fleet(id: int, session: AsyncSession = Depends(session)) -> str:
    return await delete_obj(Fleet, session, id)


# Vehicle endpoint
# -------------------------------------------------------------------------------------------------------------
api_vehicle = APIRouter(prefix="/vehicles", tags=["Vehicle"])

# Create vehicle
@api_vehicle.post("/", response_model=schemas.Vehicle)
async def create_vehicle(
    data: schemas.VehicleCreate, session: AsyncSession = Depends(session)
) -> Vehicle:
    vehicle: Vehicle = await create_vehicle_obj( session, **data.dict())
    return vehicle


# Get vehicle
@api_vehicle.get("/{id}", response_model=schemas.Vehicle)
async def get_vehicle(id: int, session: AsyncSession = Depends(session)) -> Vehicle:
    vehicle: Vehicle = await get_obj(Vehicle, session, id)
    return vehicle


# Get all vehicles
@api_vehicle.get("/", response_model=List[schemas.Vehicle])
async def get_vehicles(
    name: str = Query(None),
    fleet_id: int = Query(None),
    session: AsyncSession = Depends(session),
) -> List[Vehicle]:
    vehicle: List[Vehicle] = await get_all_vehicles_obj(session, name, fleet_id)
    return vehicle


# Update vehicle
@api_vehicle.put("/{id}")
async def update_vehicle(
    id: int, data: schemas.VehicleBase, session: AsyncSession = Depends(session)
) -> str:
    return await update_obj(Vehicle, session, id, **data.dict())


# Delete vehicle
@api_vehicle.delete("/{id}")
async def delete_vehicles(id: int, session: AsyncSession = Depends(session)) -> str:
    return await delete_obj(Vehicle, session, id)


# Driver endpoint
# -------------------------------------------------------------------------------------------------------------
api_driver = APIRouter(prefix="/drivers", tags=["Driver"])


@api_driver.post("/", response_model=schemas.Driver)
async def create_driver(
    data: schemas.DriverCreate, session: AsyncSession = Depends(session)
) -> Driver:
    driver: Driver = await create_obj(Driver, session, **data.dict())
    return driver


# Get driver by id
@api_driver.get("/{id}", response_model=schemas.Driver)
async def get_driver(id: int, session: AsyncSession = Depends(session)) -> Driver:
    driver: Driver = await get_obj(Driver, session, id)
    return driver


# Get all drivers
@api_driver.get("/", response_model=List[schemas.Driver])
async def get_drivers(
    name: str = Query(None), session: AsyncSession = Depends(session)
) -> List[Driver]:
    driver: List[Driver] = await get_all_obj(Driver, session, name)
    return driver


# Update driver
@api_driver.put("/{id}")
async def update_driver(
    id: int, data: schemas.DriverBase, session: AsyncSession = Depends(session)
) -> str:
    return await update_obj(Driver, session, id, **data.dict())


# Delete driver
@api_driver.delete("/{id}")
async def delete_driver(id: int, session: AsyncSession = Depends(session)) -> str:
    return await delete_obj(Driver, session, id)


# Route endpoint
# -------------------------------------------------------------------------------------------------------------
api_route = APIRouter(prefix="/routes", tags=["Route"])

# Create route
@api_route.post("/", response_model=schemas.Route)
async def create_route(
    data: schemas.RouteCreate, session: AsyncSession = Depends(session)
) -> Route:
    route: Route = await create_obj(Route, session, **data.dict())
    return route


# Get route
@api_route.get("/{id}", response_model=schemas.Route)
async def get_route(id: int, session: AsyncSession = Depends(session)) -> Route:
    route: Route = await get_obj(Route, session, id)
    return route


# Get all routes
@api_route.get("/", response_model=List[schemas.Route])
async def get_all_routes(
    route_name: str = Query(None),
    vehicle_name: str = Query(None),
    driver_name: str = Query(None),
    session: AsyncSession = Depends(session),
) -> List[Route]:
    route: List[Route]
    if route_name or vehicle_name or driver_name:
        route = await get_route_obj_by_name(
            session, route_name, vehicle_name, driver_name
        )
    else:
        route = await get_all_obj(Route, session, None)
    return route


# Update route
@api_route.put("/{id}")
async def update_route(
    id: int, data: schemas.RouteBase, session: AsyncSession = Depends(session)
) -> str:
    return await update_obj(Route, session, id, **data.dict())


# Delete route
@api_route.delete("/{id}")
async def delete_route(id: int, session: AsyncSession = Depends(session)) -> str:
    return await delete_obj(Route, session, id)


# RouteDetail endpoint
# -------------------------------------------------------------------------------------------------------------
api_routedetail = APIRouter(prefix="/routedetails", tags=["Route Detail"])

# Create route detail
@api_routedetail.post("/", response_model=schemas.RouteDetail)
async def create_route_detail(
    data: schemas.RouteDetailCreate, session: AsyncSession = Depends(session)
) -> RouteDetail:
    data.start_time = datetime.strptime(data.start_time, "%Y-%m-%dT%H:%M:%SZ")
    data.end_time = datetime.strptime(data.end_time, "%Y-%m-%dT%H:%M:%SZ")
    route_detail: RouteDetail = await create_obj_db(RouteDetail, session, **data.dict())
    return route_detail


# Get route detail
@api_routedetail.get("/{route_id}/{vehicle_id}", response_model=schemas.RouteDetail)
async def get_route_detail(
    route_id: int, vehicle_id: int, session: AsyncSession = Depends(session)
) -> RouteDetail:
    route_detail: RouteDetail = await get_route_detail_obj(
        session, route_id, vehicle_id
    )
    return route_detail


# Get all routes details
@api_routedetail.get("/", response_model=List[schemas.RouteDetail])
async def get_all_route_details(
    session: AsyncSession = Depends(session),
) -> List[RouteDetail]:
    route_detail: List[RouteDetail] = await get_all_obj(RouteDetail, session, None)
    return route_detail


# Update route
@api_routedetail.put("/{route_id}/{vehicle_id}")
async def update_route_detail(
    route_id: int,
    vehicle_id: int,
    data: schemas.RouteDetailBase,
    session: AsyncSession = Depends(session),
) -> str:
    return await update_route_detail_obj(session, route_id, vehicle_id, **data.dict())


# Delete route
@api_routedetail.delete("/{route_id}/{vehicle_id}")
async def delete_route_detail(
    route_id: int, vehicle_id: int, session: AsyncSession = Depends(session)
) -> str:
    return await delete_route_detail_obj(session, route_id, vehicle_id)
