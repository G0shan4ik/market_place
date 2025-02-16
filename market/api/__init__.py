from .core import app
from .routes import user_router

app.include_router(user_router)