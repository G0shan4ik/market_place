from sqlalchemy import inspect

from market.database.sql.methods.reviews import ReviewService
from .include import *
from market.database.sql.models import Review

review_router = APIRouter(
    tags=['Review']
)


@review_router.post(
    '/review/create',
    response_model=CreatedModel
)
async def create_review(
    review: ReviewCreate,
    review_db: Annotated[ReviewService, Depends(sql_helper_factory(ReviewService))]
):
    created_id: int = await review_db.create_review(review)
    return {
        'created_id': created_id
    }


@review_router.post(
    '/review/delete/{review_id}',
    response_model=StatusModel
)
async def delete_review(
    review_id: int,
    review_db: Annotated[ReviewService, Depends(sql_helper_factory(ReviewService))]
):
    status: bool = await review_db.delete_review(review_id)
    return {
        'status': status
    }


@review_router.get(
    '/review/get_review_by_id',
    response_model=ReviewResponse
)
async def get_review_by_id(
    review_id: int,
    review_db: Annotated[ReviewService, Depends(sql_helper_factory(ReviewService))]
):
    _review: Review = await review_db.get_review_by_id(review_id)
    result: dict = {}
    if _review:
        inspector = inspect(Review)
        for column in inspector.mapper.columns:
            result[column.name] = getattr(_review, column.name)

    return result


@review_router.get(
    '/review/get_reviews_by_product'
)
async def get_reviews_by_product(
    product_id: int,
    review_db: Annotated[ReviewService, Depends(sql_helper_factory(ReviewService))]
):
    _review: [Review] = await review_db.get_reviews_by_product(product_id)
    result: [ReviewResponse] = {}
    if _review:
        for review in _review:
            inspector = inspect(Review)
            dct, _key = {}, None

            for column in inspector.mapper.columns:
                if column.name == 'id':
                    _key = getattr(review, column.name)

                dct[column.name] = getattr(review, column.name)

            result[_key] = dct

    return result