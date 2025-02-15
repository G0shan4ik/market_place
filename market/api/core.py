from contextlib import asynccontextmanager
from fastapi import FastAPI
from market.database.sql.core import init_database

from os import getenv
from dotenv import load_dotenv


load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
	await init_database()
	yield


app = FastAPI(
    debug=bool(getenv("DEBUG", True)),
    lifespan=lifespan
)

__all__ = ["app"]