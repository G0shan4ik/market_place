from sqlalchemy import inspect

from market.database.sql.methods.carts import CartService
from .include import *
from market.database.sql.models import Cart, CartItem

cart_router = APIRouter(
    tags=['Cart']
)


@cart_router.post(
    '/cart/create',
    response_model=CreatedModel
)
async def create_cart(
    user_id: int,
    cart_db: Annotated[CartService, Depends(sql_helper_factory(CartService))]
):
    created_id: int = await cart_db.create_cart(user_id)
    return {
        'created_id': created_id
    }


@cart_router.post(
    '/cart/update',
    response_model=StatusModel
)
async def update_cart(
    cart_id: int,
    cart_db: Annotated[CartService, Depends(sql_helper_factory(CartService))]
):
    status: bool = await cart_db.update_cart(cart_id)
    return {
        'status': status
    }


@cart_router.post(
    '/cart/delete',
    response_model=StatusModel
)
async def delete_cart(
    cart_id: int,
    cart_db: Annotated[CartService, Depends(sql_helper_factory(CartService))]
):
    status: bool = await cart_db.delete_cart(cart_id)
    return {
        'status': status
    }


@cart_router.post(
    '/cart/cart_item/create_or_update',
    response_model=CreatedModel
)
async def create_or_update_item(
    cart_item: CartItemUpdate,
    cart_db: Annotated[CartService, Depends(sql_helper_factory(CartService))]
):
    created_id: int = await cart_db.create_or_update_item(cart_item)
    return {
        'created_id': created_id
    }


@cart_router.post(
    '/cart/cart_item/delete',
    response_model=StatusModel
)
async def delete_cart(
    cart_item: CartItemRemove,
    cart_db: Annotated[CartService, Depends(sql_helper_factory(CartService))]
):
    status: bool = await cart_db.delete_item(cart_item)
    return {
        'status': status
    }


@cart_router.get(
    '/cart/get_cart_by_id',
    response_model=CartResponse
)
async def get_cart_by_id(
        cart_id: int,
        cart_db: Annotated[CartService, Depends(sql_helper_factory(CartService))]
):
    _cart: Cart = await cart_db.get_cart_by_id(cart_id)
    result: dict = {}
    if _cart:
        inspector = inspect(Cart)
        for column in inspector.mapper.columns:
            result[column.name] = getattr(_cart, column.name)

    return result


@cart_router.get(
    '/cart/cart_item/get_item_by_id',
    response_model=CartItemResponse
)
async def get_cart_by_id(
        cart_item_id: int,
        cart_db: Annotated[CartService, Depends(sql_helper_factory(CartService))]
):
    _cart_item: CartItem = await cart_db.get_item_by_id(cart_item_id)
    result: dict = {}
    if _cart_item:
        inspector = inspect(CartItem)
        for column in inspector.mapper.columns:
            result[column.name] = getattr(_cart_item, column.name)

    return result


@cart_router.get('/cart/cart_item/get_items')
async def get_items(
        cart_item: CartItemsIds,
        cart_db: Annotated[CartService, Depends(sql_helper_factory(CartService))]
):
    _cart_items: [CartItem] = await cart_db.get_items(cart_item)
    result: dict = {}
    if _cart_items:
        for item in _cart_items:
            inspector = inspect(CartItem)
            dct, _key = {}, None

            for column in inspector.mapper.columns:
                if column.name == 'id':
                    _key = getattr(item, column.name)

                dct[column.name] = getattr(item, column.name)

            result[_key] = dct

    return result
