from fastapi import FastAPI
from database import async_db_session

app = FastAPI()


@app.on_event("startup")
async def startup():
    await async_db_session.init()
    await async_db_session.create_all()

@app.on_event("shutdown")
async def shutdown():
    await async_db_session.close()

from services import *

sv = [api_fleet, api_vehicle, api_vehicle,api_driver, api_route]

app.include_router(api_fleet)
app.include_router(api_vehicle)