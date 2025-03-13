from sqlalchemy import inspect

from market.database.sql.methods.payments import PaymentService
from .include import *
from market.database.sql.models import Payment

payment_router = APIRouter(
    tags=['Payment']
)


@payment_router.post(
    '/payment/create',
    response_model=CreatedModel
)
async def create_payment(
    payment: PaymentCreate,
    payment_db: Annotated[PaymentService, Depends(sql_helper_factory(PaymentService))]
):
    created_id: int = await payment_db.create_payment(payment)
    return {
        'created_id': created_id
    }


@payment_router.post(
    '/payment/update',
    response_model=StatusModel
)
async def update_payment(
    payment_id: int,
    status: PaymentStatus,
    payment_db: Annotated[PaymentService, Depends(sql_helper_factory(PaymentService))]
):
    status: bool = await payment_db.update_payment_status(payment_id, status)
    return {
        'status': status
    }


@payment_router.get(
    '/payment/get_payment_by_id',
    response_model=PaymentResponse
)
async def get_payment_by_id(
        payment_id: int,
        payment_db: Annotated[PaymentService, Depends(sql_helper_factory(PaymentService))]
):
    _payment: Payment = await payment_db.get_payment_by_id(payment_id)
    result: dict = {}
    if _payment:
        inspector = inspect(Payment)
        for column in inspector.mapper.columns:
            result[column.name] = getattr(_payment, column.name)

    return result