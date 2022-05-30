from typing import AsyncGenerator
from asyncio import current_task
from sqlalchemy import true
from ..src.controller import *
from ..src.schemas import *
from ..src.models import *
from ..src import settings
import pytest
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine,AsyncSession,async_scoped_session

@pytest.fixture()
async def test_session() -> AsyncGenerator[AsyncSession, None]:
    engine = create_async_engine(
            "postgresql+asyncpg://postgres:postgres@localhost/fleet_db",
            echo=False,
            # pool_size=20, max_overflow=0
        )
    # async with engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.drop_all)
    #     await conn.run_sync(Base.metadata.create_all)

    # expire_on_commit=False will prevent attributes from being expired
    # after commit.
    session_maker = sessionmaker(
        bind=engine, expire_on_commit=False, class_=AsyncSession
    )
    Session = async_scoped_session(session_maker , scopefunc=current_task)
    async with Session() as session:
        yield session
        

@pytest.mark.parametrize("name,description",[
    ("Test Fleet 1", "Test Fleet Description 1"),
    ("Test Fleet 2", "Test Fleet Description 2"),
    ("Test Fleet 3", "Test Fleet Description 3")
])
@pytest.mark.asyncio
async def test_create_fleet(name:str,description:str,test_session):
    fleet = FleetCreate(name = name, description=description)
    result = await create_obj(Fleet,test_session,**fleet.dict())
    assert result == "Created Successfully"
    