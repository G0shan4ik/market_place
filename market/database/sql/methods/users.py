from .include import Users, AsyncSession, select, insert, logger


async def create_user(
        session: AsyncSession,
        user_id: int
):
    stmt = insert(Users).values(Users_id=user_id)
    result = await session.execute(stmt)
    await session.commit()

    logger.debug(f"create_user: {stmt}")

    return result

async def get_or_create_user(session: AsyncSession, user_id: int) -> Users:
    stmt = select(Users).where(
        user_id == Users.id
    )

    result = await session.execute(stmt)
    result = result.scalar()
    if not result:
        result = await create_user(
            session=session,
            user_id=user_id
        )
        await session.commit()

    return result
