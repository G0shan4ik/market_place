from sqlalchemy import inspect

from market.database.sql.methods.users import UserService
from .include import *
from market.database.sql.models import User

user_router = APIRouter(
    tags=['Users']
)


@user_router.post(
    '/user/login',
    response_model=CreatedModel
)
async def create_account(
    user: UserCreate,
    user_db: Annotated[UserService, Depends(sql_helper_factory(UserService))]
):
    created_id: int = await user_db.create_buyer(user)
    return {
        'created_id': created_id
    }


@user_router.post(
    '/user/sign_in',
    response_model=ActiveModel
)
async def sign_in_account(
    user: UserActive,
    user_db: Annotated[UserService, Depends(sql_helper_factory(UserService))]
):
    status_data: dict = await user_db.sign_in(user)
    return status_data


@user_router.post('/user/delete_user/{user_id}')
async def delete_account(
        user_id: int,
        user_db: Annotated[UserService, Depends(sql_helper_factory(UserService))]
):
    result: bool = await user_db.deactivate_user(user_id)
    return {
        'status': result
    }


@user_router.get('/user/get_user_by_id/{user_id}')
async def get_user_by_id(
        user_id: int,
        user_db: Annotated[UserService, Depends(sql_helper_factory(UserService))]
):
    _user: User = await user_db.get_by_id(user_id)
    result: dict = {}
    if _user:
        inspector = inspect(User)
        for column in inspector.mapper.columns:
            result[column.name] = getattr(_user, column.name)

    return result


@user_router.post('/update_user')  # Сделать проверки на всякую хуету
async def update_user_data(
    user_id: int,
    user: UserRequestUpdate,
    user_db: Annotated[UserService, Depends(sql_helper_factory(UserService))]
):
    await user_db.update_user(user_id, **user.model_dump(exclude_unset=True))

@user_router.get('/user/get_user_by_role/')
async def get_user_by_role(
        user_role: UserRole,
        user_db: Annotated[UserService, Depends(sql_helper_factory(UserService))],
        page: int = 1,
        per_page: int = 10,
):
    _users: list[User] = await user_db.get_by_role(role=user_role, page=page, per_page=per_page)
    result: dict = {}
    if _users:
        for user in _users:
            inspector = inspect(User)
            dct, _key = {}, None

            for column in inspector.mapper.columns:
                if column.name == 'id':
                    _key = getattr(user, column.name)

                dct[column.name] = getattr(user, column.name)

            result[_key] = dct

    return result


@user_router.post(
    '/user/promote_to_seller',
    response_model=CreatedModel
)
async def create_seller(
    user: UserSeller,
    user_db: Annotated[UserService, Depends(sql_helper_factory(UserService))]
):
    created_id: int = await user_db.promote_to_seller(user)
    return {
        'created_id': created_id
    }
