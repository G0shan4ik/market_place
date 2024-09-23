import asyncio
from market.database.sql.core import init


def start_test():
    asyncio.run(init())