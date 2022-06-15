from fastapi import FastAPI
from .session import engine
from .models import Base


app = FastAPI()

@app.get("/")
async def root() -> str:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    return "Connect successfully"

from .view import *

sv = [api_fleet, api_vehicle, api_driver, api_route, api_routedetail]

for service in sv:
    app.include_router(service)
