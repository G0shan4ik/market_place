from sqlalchemy import inspect

from market.database.sql.methods.orders import OrderService
from .include import *
from market.database.sql.models import Order, OrderItem

order_router = APIRouter(
    tags=['Order']
)


@order_router.post(
    '/order/create',
    response_model=CreatedModel
)
async def create_order(
    order: OrderCreate,
    order_db: Annotated[OrderService, Depends(sql_helper_factory(OrderService))]
):
    created_id: int = await order_db.create_order(order)
    return {
        'created_id': created_id
    }


@order_router.post(
    '/order/update_order_status',
    response_model=StatusModel
)
async def update_order_status(
    order_id: int,
    _status: OrderStatus,
    order_db: Annotated[OrderService, Depends(sql_helper_factory(OrderService))]
):
    status: bool = await order_db.update_order_status(order_id, _status)
    return {
        'status': status
    }


@order_router.post(
    '/order/delete',
    response_model=StatusModel
)
async def delete_order(
    order_id: int,
    order_db: Annotated[OrderService, Depends(sql_helper_factory(OrderService))]
):
    status: bool = await order_db.delete_order(order_id)
    return {
        'status': status
    }


@order_router.post(
    '/order/order_item/add_order_item',
    response_model=CreatedModel
)
async def add_order_item(
    order_item: OrderItemCreate,
    order_db: Annotated[OrderService, Depends(sql_helper_factory(OrderService))]
):
    created_id: int = await order_db.add_order_item(order_item)
    return {
        'created_id': created_id
    }


@order_router.post(
    '/order/order_item/update_quantity',
    response_model=StatusModel
)
async def update_order_item_quantity(
    item_id: int,
    quantity: int,
    order_db: Annotated[OrderService, Depends(sql_helper_factory(OrderService))]
):
    status: bool = await order_db.update_order_item_quantity(item_id, quantity)
    return {
        'status': status
    }


@order_router.post(
    '/order/order_item/delete',
    response_model=StatusModel
)
async def delete_order_item(
    item_id: int,
    order_db: Annotated[OrderService, Depends(sql_helper_factory(OrderService))]
):
    status: bool = await order_db.delete_order_item(item_id)
    return {
        'status': status
    }


@order_router.get(
    '/user/get_order_by_id',
    response_model=OrderResponse
)
async def get_order_by_id(
        order_id: int,
        order_db: Annotated[OrderService, Depends(sql_helper_factory(OrderService))]
):
    _order: Order = await order_db.get_order_by_id(order_id)
    result: dict = {}
    if _order:
        inspector = inspect(Order)
        for column in inspector.mapper.columns:
            result[column.name] = getattr(_order, column.name)

    return result


@order_router.get(
    '/user/order_item/get_item_by_id',
    response_model=OrderItemResponse
)
async def get_item_by_id(
        order_item_id: int,
        order_db: Annotated[OrderService, Depends(sql_helper_factory(OrderService))]
):
    _order_item: OrderItem = await order_db.get_item_by_id(order_item_id)
    result: dict = {}
    if _order_item:
        inspector = inspect(OrderItem)
        for column in inspector.mapper.columns:
            result[column.name] = getattr(_order_item, column.name)

    return result


@order_router.get('/user/get_orders_by_buyer')
async def get_orders_by_buyer(
        buyer_id: int,
        order_db: Annotated[OrderService, Depends(sql_helper_factory(OrderService))]
):
    _order_buyer: Optional[dict] = await order_db.get_orders_by_buyer(buyer_id)

    return _order_buyer


@order_router.get(
    '/user/order_item/get_items',
    response_model=OrderItemResponse
)
async def get_order_items(
        order_id: int,
        order_db: Annotated[OrderService, Depends(sql_helper_factory(OrderService))]
):
    _order_items: [OrderItem] = await order_db.get_order_items(order_id)
    result: dict = {}
    if _order_items:
        for item in _order_items:
            inspector = inspect(OrderItem)
            dct, _key = {}, None

            for column in inspector.mapper.columns:
                if column.name == 'id':
                    _key = getattr(item, column.name)

                dct[column.name] = getattr(item, column.name)

            result[_key] = dct

    return result


