from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine,AsyncSession


async def async_db_session() -> Generator:
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