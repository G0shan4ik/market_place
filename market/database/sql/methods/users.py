from .include import User, UserRole, select, update, insert, BaseDatabaseDep, UserCreate, UserSeller, UserActive, Optional


class UserService(BaseDatabaseDep):
    async def create_buyer(self, user: UserCreate) -> int:
        temp_user = User()
        temp_user.password = user.password
        password_hash = temp_user.password_hash

        stmt = select(User).where(
            User.email == user.email).where(
            User.is_active == True
        )
        result = (await self.session.execute(stmt)).scalar_one_or_none()
        assert result, 'Пользователь уже зарегистрирован!'

        stmt = insert(User).values(
            username=user.username,
            email=user.email,
            password_hash=password_hash,
            role=UserRole.BUYER.value,
            is_active=True,
        ).returning(User.id)

        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.scalar()

    async def sign_in(self, user: UserActive) -> Optional[dict]:
        """
            Sign in account
        :param user:
        :return: dict { key: role, key: username }
        """
        stmt = select(User).where(
            User.email == user.email
        )
        result = (await self.session.execute(stmt)).scalar_one_or_none()
        assert result, 'Пользователя не существует!'

        check_valid_pass: bool = User().check_password(
            simple_password=user.password,
            hashed_password=result.password_hash
        )
        assert check_valid_pass, 'Неверный пароль!'

        assert result.is_active, 'Аккаунт пользователя удален'
        return {
            'id': result.id,
            'role': result.role,
            'username': result.username,
            'is_active': result.is_active
        }

    async def deactivate_user(self, user_id: int) -> bool:
        try:
            stmt = (
                update(User)
                .where(User.id == user_id)
                .values(is_active=False)
            )
            await self.session.execute(stmt)
            await self.session.commit()

            return True
        except Exception as ex:
            raise Exception(ex)

    async def get_by_id(self, user_id: int) -> Optional[User]:
        stmt = select(User).where(
            User.id == user_id
        )
        result = (await self.session.execute(stmt)).scalar_one_or_none()

        assert result, f'Пользователя с ID == {user_id} не существует!'
        return result

    async def update_user(self, user_id: int, data: dict) -> bool:
        result = await self.get_by_id(user_id)

        if result:
            allowed_fields = {
                "username",
                "email",
                "phone_number",
                "company_name",
                "tax_id"
            }
            update_data = {k: v for k, v in data.items() if k in allowed_fields}

            assert update_data, "Нет полей для обновления"

            stmt = (
                update(User)
                .where(User.id == user_id)
                .values(**update_data)
            )
            await self.session.execute(stmt)
            await self.session.commit()

            return True
        raise ValueError('Пользователь не найден!')

    async def promote_to_seller(self, user: UserSeller) -> int:
        stmt = update(User).where(
            User.id == user.id
        ).values(
                role=UserRole.SELLER,
                company_name=user.company_name,
                tax_id=user.tax_id,
                phone_number=user.phone_number
        ).returning(User.id)

        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.scalar()

    async def get_by_role(self, role: UserRole, page: int = 1, per_page: int = 10) -> [User]:
        offset = (page - 1) * per_page
        stmt = (
            select(User)
            .where(User.role == role)
            .offset(offset)
            .limit(per_page)
        )
        result = await self.session.execute(stmt)

        return result.scalars().all()