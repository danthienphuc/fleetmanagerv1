from asyncio import current_task
from typing import AsyncGenerator
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_scoped_session,
)


engine = create_async_engine(
    "postgresql+asyncpg://postgres:postgres@localhost/fleet_db",
    echo=False,
    # pool_size=20, max_overflow=0
)


async def async_db_session() -> AsyncGenerator[AsyncSession, None]:

    # expire_on_commit=False will prevent attributes from being expired
    # after commit.
    session_maker = sessionmaker(
        bind=engine, expire_on_commit=False, class_=AsyncSession
    )
    Session = async_scoped_session(session_maker, scopefunc=current_task)
    async with Session() as session:
        yield session
