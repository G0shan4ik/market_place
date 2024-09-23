from .include import *


class MarketUsers(BaseDatabaseDep):
    @staticmethod
    async def create_user(
            session: AsyncSession,
            user_id: int
    ):
        stmt = insert(Users).values(Users_id=user_id)
        result = await session.execute(stmt)
        await session.commit()

        logger.debug(f"create_user: {stmt}")

        return result

    async def get_or_create_user(self, user_id: int) -> Users:
        stmt = select(Users).where(
            user_id == Users.id
        )

        result = await self.session.execute(stmt)
        result = result.scalar()
        if not result:
            result = await self.create_user(
                session=self.session,
                user_id=user_id
            )
            await self.session.commit()

        return result
