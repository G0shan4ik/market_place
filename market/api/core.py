from .routes import router
from fastapi import FastAPI
from subprocess import call

app = FastAPI()
app.include_router(router)


def start_server():
    call(["uvicorn", "resys:app", "--reload", "--host=0.0.0.0"])


__all__ = ["start_server", "app"]