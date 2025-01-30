import asyncio
from market.database.sql.core import init
from subprocess import run
from market.api.core import app


# def start_test():
#     asyncio.run(init())


def start_dev():
    run(["uvicorn", "main:app", "--reload", "--host=127.0.0.1", "--port=8000", "--reload"])


if __name__ == '__main__':
    init()