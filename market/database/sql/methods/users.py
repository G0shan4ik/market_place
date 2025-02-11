from datetime import datetime
from typing import Optional, Dict, List

from market.api.datamodels import UserSeller
from .include import User, UserRole, select, update, insert, BaseDatabaseDep, UserCreate


class UserService(BaseDatabaseDep):
    async def create_buyer(self, user: UserCreate) -> int:
        temp_user = User()
        temp_user.password = user.password
        password_hash = temp_user.password_hash

        stmt = insert(User).values(
            username=user.username,
            email=user.email,
            password_hash=password_hash,
            role=UserRole.BUYER,
            is_active=True,
            phone_number=user.phone_number,
        ).returning(User.id)

        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.scalar()

    async def deactivate_user(self, user_id: int) -> None:
        stmt = (
            update(User)
            .where(User.id == user_id)
            .values(is_active=False)
        )
        await self.session.execute(stmt)
        await self.session.commit()

    async def get_by_id(self, user_id: int) -> Optional[User]:
        stmt = (
            select(User)
            .where(User.id == user_id)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def update_user(self, user_id: int, **data: Dict) -> None:
        allowed_fields = {
            "username",
            "email",
            "phone_number",
            "company_name",
            "tax_id"
        }
        update_data = {k: v for k, v in data.items() if k in allowed_fields}

        if not update_data:
            raise ValueError("Нет полей для обновления")

        stmt = (
            update(User)
            .where(User.id == user_id)
            .values(**update_data)
        )
        await self.session.execute(stmt)
        await self.session.commit()

    async def promote_to_seller(self, user: UserSeller) -> None:
        stmt = (
            update(User)
            .where(User.id == user.id)
            .values(
                role=UserRole.SELLER,
                company_name=user.company_name,
                tax_id=user.tax_id
            )
        )
        await self.session.execute(stmt)
        await self.session.commit()

    async def get_by_role(
            self,
            role: UserRole,
            page: int = 1,
            per_page: int = 10
    ) -> list[User]:
        offset = (page - 1) * per_page
        stmt = (
            select(User)
            .where(User.role == role)
            .offset(offset)
            .limit(per_page)
        )
        result = await self.session.execute(stmt)
        print('\n\n', result, '\n', await self.session.stream_scalars(stmt), '\n', result.scalars().all(), '\n', result.scalars(), '\n\n')
        return result.scalars().all()