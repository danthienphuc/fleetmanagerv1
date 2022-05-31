from fastapi import FastAPI
from src.session import engine,Base

app = FastAPI()
    
    
async def refresh():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@app.get("/")
async def root():
    return "Connect successfully"



from .view import *

sv = [api_fleet, api_vehicle, api_driver, api_route, api_routedetail]

for service in sv:
    app.include_router(service)