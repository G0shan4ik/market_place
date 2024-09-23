from typing import Type, TypeVar

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import Annotated

from .core import session_maker
from .methods.base import BaseDatabaseDep


dependent_type = TypeVar('dependent_type', bound=Type[BaseDatabaseDep])


async def get_session():
    async with session_maker() as session:
        yield session


def sql_helper_factory(_dep: Type[dependent_type]):
    async def dep(session: Annotated[AsyncSession, Depends(get_session)] = None) -> dependent_type:
        if session is None:
            async with session_maker() as session:
                instance = _dep(session)
                yield instance
        else:
            instance = _dep(session)
            yield instance

    return dep


__all__ = [
    'sql_helper_factory'
]