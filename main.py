import asyncio
from typing import List
from fastapi import FastAPI
from database import async_db_session

import schemas, models

app = FastAPI()


# Fleet endpoint

# Create fleet
@app.post("/fleets")
async def create_fleet(data: schemas.FleetCreate):
    return await models.Fleet.create(**data.dict())

# Get fleet
@app.get("/fleets/{id}", response_model=schemas.Fleet)
async def get_fleet(id: int):
    return await models.Fleet.get(id)

# Get all fleets
@app.get("/fleets", response_model=List(schemas.Fleet))
async def get_fleets():
    return await models.Fleet.get_all()

# Update fleet
@app.put("/fleets/{id}")
async def update_fleet(id: int, data: schemas.Fleet):
    return await models.Fleet.update(id, **data.dict())

# Delete fleet
@app.delete("/fleets/{id}")
async def delete_fleet(id: int):
    return await models.Fleet.delete(id)

# Vehicle endpoint

# Create vehicle
@app.post("/vehicles")
async def create_vehicle(data: schemas.VehicleCreate):
    return await models.Vehicle.create(**data.dict())

# Get vehicle
@app.get("/vehicles/{id}", response_model=schemas.Vehicle)
async def get_vehicle(id: int):
    return await models.Vehicle.get(id)

# Get all vehicles
@app.get("/vehicles", response_model=List(schemas.Vehicle))
async def get_vehicles():
    return await models.Vehicle.get_all()

# Update vehicle
@app.put("/vehicles/{id}")
async def update_vehicle(data: schemas.Vehicle):
    return await models.Vehicle.update(id,data.dict())

# Delete vehicle
@app.delete("vehicles")
async def delete_vehicles(id:int):
    return await models.Vehicle.delete(id)

# Driver endpoint

# Create driver
@app.post("/drivers")
async def create_driver(data: schemas.DriverCreate):
    return await models.Driver.update(id,data.dict())




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