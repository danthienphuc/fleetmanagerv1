from fastapi import FastAPI
from .session import engine
from .models import Base


app = FastAPI()
    

# Base.metadata.drop_all(bind=engine)
# Base.metadata.create_all(bind=engine)

# @app.on_event("startup")  
# async def refresh():
#     async with engine.begin() as conn:
#         # await conn.run_sync(Base.metadata.drop_all)
#         await conn.run_sync(Base.metadata.create_all)

@app.get("/")
async def root():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    return "Connect successfully"



from .view import *

sv = [api_fleet, api_vehicle, api_driver, api_route, api_routedetail]

for service in sv:
    app.include_router(service)