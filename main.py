import asyncio
import sys

from market.api.core import app


def start_dev():
    from subprocess import run
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    run(["uvicorn", "main:app", "--reload", "--host=0.0.0.0", "--port=8000", "--reload"])