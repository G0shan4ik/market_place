from sqlalchemy import inspect

from market.database.sql.methods.products import ProductService
from .include import *
from market.database.sql.models import Product

product_router = APIRouter(
    tags=['Product']
)


@product_router.post(
    '/product/create',
    response_model=CreatedModel
)
async def create_product(
    product: ProductCreate,
    product_db: Annotated[ProductService, Depends(sql_helper_factory(ProductService))]
):
    created_id: int = await product_db.create_product(product)
    return {
        'created_id': created_id
    }


@product_router.post(
    '/product/update',
    response_model=StatusModel
)
async def update_product(
    product_id: int,
    product: ProductUpdate,
    product_db: Annotated[ProductService, Depends(sql_helper_factory(ProductService))]
):
    status: bool = await product_db.update_product(product_id, **product.model_dump(exclude_unset=True))
    return {
        'status': status
    }


@product_router.post(
    '/product/delete',
    response_model=CreatedModel
)
async def delete_product(
    product_id: int,
    product_db: Annotated[ProductService, Depends(sql_helper_factory(ProductService))]
):
    created_id: int = await product_db.delete_product(product_id)
    return {
        'created_id': created_id
    }


@product_router.get(
    '/product/get_by_id',
    response_model=ProductResponse
)
async def get_product_by_id(
    product_id: int,
    product_db: Annotated[ProductService, Depends(sql_helper_factory(ProductService))]
):
    _product: Product = await product_db.get_product_by_id(product_id)
    result: dict = {}
    if _product:
        inspector = inspect(Product)
        for column in inspector.mapper.columns:
            result[column.name] = getattr(_product, column.name)

    return result


@product_router.get('/product/get_by_category')
async def get_products_by_category(
    category_id: int,
    product_db: Annotated[ProductService, Depends(sql_helper_factory(ProductService))]
):
    _product: [Product] = await product_db.get_products_by_category(category_id)
    result = {}
    if _product:
        for product in _product:
            inspector = inspect(Product)
            dct, _key = {}, None

            for column in inspector.mapper.columns:
                if column.name == 'id':
                    _key = getattr(product, column.name)

                dct[column.name] = getattr(product, column.name)

            result[_key] = dct

    return result