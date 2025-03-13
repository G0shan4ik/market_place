from .core import app
from .routes import user_router, review_router

app.include_router(user_router)
app.include_router(review_router)