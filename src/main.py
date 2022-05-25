from fastapi import FastAPI
from .database import async_db_session

app = FastAPI()


@app.on_event("startup")
async def startup():
    await async_db_session.init()
    await async_db_session.create_all()

@app.on_event("shutdown")
async def shutdown():
    await async_db_session.close()

from .services import *

sv = [api_fleet, api_vehicle, api_driver, api_route, api_routedetail]

for service in sv:
    app.include_router(service)