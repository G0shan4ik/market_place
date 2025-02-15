import sys

from sqlalchemy.orm import DeclarativeBase, declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from loguru import logger

from os import getenv
from dotenv import load_dotenv

load_dotenv()


USER = getenv("POSTGRES_USER") or None
PASSWORD = getenv("POSTGRES_PASSWORD") or None
HOST = getenv("POSTGRES_HOST")
PORT = getenv("POSTGRES_PORT")
DB = getenv("POSTGRES_DB")

uri = f"{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}"
print(f"postgresql+psycopg_async://{uri}")

engine = create_async_engine(
    url=f"postgresql+psycopg_async://{uri}",
    echo=True
)

Base: DeclarativeBase = declarative_base()
session_maker: async_sessionmaker[AsyncSession] = async_sessionmaker(bind=engine)


async def init_database():
    async with engine.connect() as connection:  # engine.begin()

        # await connection.run_sync(Base.metadata.drop_all)

        await connection.run_sync(Base.metadata.create_all)
        logger.debug(
            "Created tables: " + (", ".join(i for i in Base.metadata.tables))
        )
        await connection.commit()


async def init():
    await init_database()


if __name__ == '__main__':
    import asyncio

    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(init())