from .config import settings
from sqlalchemy.orm import DeclarativeBase, declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from loguru import logger


engine = create_async_engine(
    url=settings.db_url_asyncpg,
    echo=True
)

Base: DeclarativeBase = declarative_base()
session_maker: async_sessionmaker[AsyncSession] = async_sessionmaker(bind=engine)


async def create_tables():
    async with engine.connect() as connection:  # engine.begin()
        await connection.run_sync(Base.metadata.create_all)
        logger.debug(
            "Created tables: " + (", ".join(i for i in Base.metadata.tables))
        )
        await connection.commit()


async def init():
    await create_tables()