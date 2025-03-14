from .include import Address, AddressCreate, select, delete, update, insert, BaseDatabaseDep, Optional


class AddressService(BaseDatabaseDep):
    async def create_address(self, address: AddressCreate) -> int:
        stmt = insert(Address).values(
            street = address.street,
            city = address.city,
            state = address.state,
            postal_code = address.postal_code,
            country = address.country,
            user_id = address.user_id
        ).returning(Address.id)

        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.scalar()

    async def get_user_address(self, user_id: int) -> Optional[Address]:
        stmt = select(Address).where(
            Address.user_id == user_id
        )
        return (await self.session.execute(stmt)).scalar_one_or_none()

    async def get_address_by_id(self, address_id: int) -> Optional[Address]:
        stmt = select(Address).where(
            Address.id == address_id
        )
        return (await self.session.execute(stmt)).scalar_one_or_none()

    async def update_address(self, address_id: int, **data: dict) -> bool:
        address = self.get_address_by_id(address_id=address_id)
        if address:
            allowed_fields = {
                "street",
                "city",
                "state",
                "postal_code",
                "country"
            }
            update_data = {k: v for k, v in data.items() if k in allowed_fields}

            if not update_data:
                raise ValueError("Нет полей для обновления")

            stmt = (
                update(Address)
                .where(Address.id == address_id)
                .values(**update_data)
            )
            await self.session.execute(stmt)
            await self.session.commit()

            return True
        raise ValueError('Адрес не найден!')

    async def delete_address(self, address_id: int) -> bool:
        address = self.get_address_by_id(address_id=address_id)
        if address:
            stmt = delete(Address).where(Address.id == address_id)

            await self.session.execute(stmt)
            await self.session.commit()
            return True
        return False