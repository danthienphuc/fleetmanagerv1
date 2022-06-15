import json
import os
from typing import List
from unittest import result
import pytest
from fastapi import Depends
from ..src.models import *
from sqlalchemy.ext.asyncio import AsyncSession
from ..src.session import async_db_session as session

# Load the JSON file
def read_json()->dict:
    with open(os.path.join(os.path.dirname(__file__),'data.json') )as json_file:
        raw = json.load(json_file)
        return raw

# Map the JSON data to the model

# Fleets
def map_fleets(raw:dict)->List[Fleet]:
    fleets = []
    for fleet in raw['fleets']:
        fleets.append(Fleet(**fleet))
    return fleets

# Vehicles
def map_vehicles(raw:dict)->List[Vehicle]:
    vehicles = []
    for vehicle in raw['vehicles']:
        vehicles.append(Vehicle(**vehicle))
    return vehicles

# Drivers
def map_drivers(raw:dict)->List[Driver]:
    drivers = []
    for driver in raw['drivers']:
        drivers.append(Driver(**driver))
    return drivers

# Routes
def map_routes(raw:dict)->List[Route]:
    routes = []
    for route in raw['routes']:
        routes.append(Route(**route))
    return routes

# Route Details
def map_route_details(raw:dict)->List[RouteDetail]:
    route_details = []
    for route_detail in raw['route_details']:
        route_details.append(RouteDetail(**route_detail))
    return route_details

# Fixture to load the JSON data, map it to the model and implementation in database
@pytest.fixture
async def load_json(session: AsyncSession = Depends(session)) -> None:
    raw = read_json()
    fleets = map_fleets(raw)
    vehicles = map_vehicles(raw)
    drivers = map_drivers(raw)
    routes = map_routes(raw)
    route_details = map_route_details(raw)
    session.add_all(fleets)
    session.add_all(vehicles)
    session.add_all(drivers)
    session.add_all(routes)
    session.add_all(route_details)
    await session.commit()