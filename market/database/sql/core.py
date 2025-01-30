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
print(uri)

engine = create_async_engine(
    url=f"postgresql+psycopg_async://{uri}",
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