from sqlalchemy import inspect

from market.database.sql.methods.categories import CategoryService
from .include import *
from market.database.sql.models import Category

category_router = APIRouter(
    tags=['Category']
)


@category_router.post(
    '/category/create',
    response_model=CreatedModel
)
async def create_category(
    category: CreateCategory,
    category_db: Annotated[CategoryService, Depends(sql_helper_factory(CategoryService))]
):
    created_id: int = await category_db.create_category(category)
    return {
        'created_id': created_id
    }


@category_router.post(
    '/category/update',
    response_model=StatusModel
)
async def update_category(
    category_id: int,
    category: UpdateCategory,
    category_db: Annotated[CategoryService, Depends(sql_helper_factory(CategoryService))]
):
    status: bool = await category_db.update_category(category_id, **category.model_dump(exclude_unset=True))
    return {
        'status': status
    }


@category_router.post(
    '/category/delete',
    response_model=StatusModel
)
async def delete_category(
    category_id: int,
    category_db: Annotated[CategoryService, Depends(sql_helper_factory(CategoryService))]
):
    status: bool = await category_db.delete_category(category_id)
    return {
        'status': status
    }


@category_router.get(
    '/category/get_category',
    response_model=CategoryResponse
)
async def get_category_by_id(
        category_id: int,
        category_db: Annotated[CategoryService, Depends(sql_helper_factory(CategoryService))]
):
    _category: Category = await category_db.get_category_by_id(category_id)
    result: dict = {}
    if _category:
        inspector = inspect(Category)
        for column in inspector.mapper.columns:
            result[column.name] = getattr(_category, column.name)

    return result


@category_router.get('/category/get_all_categories')
async def get_all_categories(
        category_db: Annotated[CategoryService, Depends(sql_helper_factory(CategoryService))],
        limit: Optional[int] = None
):
    _categories: [Category] = await category_db.get_all_categories(limit)
    result: dict = {}
    if _categories:
        for category in _categories:
            inspector = inspect(Category)
            dct, _key = {}, None

            for column in inspector.mapper.columns:
                if column.name == 'id':
                    _key = getattr(category, column.name)

                dct[column.name] = getattr(category, column.name)

            result[_key] = dct

    return result


@category_router.get('/category/get_child_categories')
async def get_child_categories(
        parent_id: int,
        category_db: Annotated[CategoryService, Depends(sql_helper_factory(CategoryService))]
):
    _categories: [Category] = await category_db.get_child_categories(parent_id)
    result: dict = {}
    if _categories:
        for category in _categories:
            inspector = inspect(Category)
            dct, _key = {}, None

            for column in inspector.mapper.columns:
                if column.name == 'id':
                    _key = getattr(category, column.name)

                dct[column.name] = getattr(category, column.name)

            result[_key] = dct

    return result
