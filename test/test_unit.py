from typing import Generator
from unittest import result
from ..src.services import *
from ..src.schemas import *
import pytest
from sqlalchemy.orm import sessionmaker
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine,AsyncSession


@pytest.fixture()
async def async_session() -> Generator:
    test_engine = create_async_engine(
            "postgresql+asyncpg://postgres:postgres@localhost/fleet_db",
            echo=False,
            pool_size=20, max_overflow=0
        )
        
    # expire_on_commit=False will prevent attributes from being expired
    # after commit.
    async_sess = sessionmaker(
        test_engine, expire_on_commit=False, class_=AsyncSession
    )
    yield async_sess

@pytest.mark.asyncio
async def test_create_fleet(async_session):
    fleet = FleetCreate(name = "Fleet 1", description="gfdsg")
    result = await create_fleet(fleet,async_session)
    assert result == "Created Successfully"
    