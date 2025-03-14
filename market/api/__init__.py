from .core import app
from .routers import (
    user_router,
    product_router,
    review_router,
    payment_router,
    order_router,
    category_router
)

app.include_router(user_router)
app.include_router(product_router)
app.include_router(review_router)
app.include_router(payment_router)
app.include_router(order_router)
app.include_router(category_router)