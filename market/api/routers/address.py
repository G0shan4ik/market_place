from sqlalchemy import inspect

from market.database.sql.methods.addresses import AddressService
from .include import *
from market.database.sql.models import Address

address_router = APIRouter(
    tags=['Address']
)


@address_router.post(
    '/address/create',
    response_model=CreatedModel
)
async def create_account(
    address: AddressCreate,
    address_db: Annotated[AddressService, Depends(sql_helper_factory(AddressService))]
):
    created_id: int = await address_db.create_address(address)
    return {
        'created_id': created_id
    }


@address_router.post(
    '/address/delete',
    response_model=StatusModel
)
async def delete_address(
    address_id: int,
    address_db: Annotated[AddressService, Depends(sql_helper_factory(AddressService))]
):
    status: bool = await address_db.delete_address(address_id)
    return {
        'status': status
    }


@address_router.post(
    '/address/update',
    response_model=StatusModel
)
async def update_address(
    address_id: int,
    address: AddressUpdate,
    address_db: Annotated[AddressService, Depends(sql_helper_factory(AddressService))]
):
    status: bool = await address_db.update_address(address_id, address.model_dump(exclude_unset=True))
    return {
        'status': status
    }


@address_router.get(
    '/address/get_user_address',
    response_model=AddressResponse
)
async def get_user_address(
        user_id: int,
        address_db: Annotated[AddressService, Depends(sql_helper_factory(AddressService))]
):
    _address: Address = await address_db.get_user_address(user_id)
    result: dict = {}
    if _address:
        inspector = inspect(Address)
        for column in inspector.mapper.columns:
            result[column.name] = getattr(_address, column.name)

    return result


@address_router.get(
    '/address/get_address',
    response_model=AddressResponse
)
async def get_address_by_id(
        address_id: int,
        address_db: Annotated[AddressService, Depends(sql_helper_factory(AddressService))]
):
    _address: Address = await address_db.get_address_by_id(address_id)
    result: dict = {}
    if _address:
        inspector = inspect(Address)
        for column in inspector.mapper.columns:
            result[column.name] = getattr(_address, column.name)

    return result