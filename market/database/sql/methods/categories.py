from market.database.sql.models import Category
from typing import Optional

from .include import select, update, delete, insert, BaseDatabaseDep, CreateCategory

class CategoryService(BaseDatabaseDep):
    async def create_category(self, category: CreateCategory) -> int:
        stmt = select(Category).where(
            Category.name == category.name).where(
        )
        result = (await self.session.execute(stmt)).scalar_one_or_none()
        if result:
            raise ValueError(f'{"Подкатегория" if category.parent_id else "Категория"} уже существует!')

        stmt = insert(Category).values(
            name=category.name,
            parent_id=category.parent_id
        ).returning(Category.id)

        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.scalar()

    async def get_category_by_id(self, category_id: int) -> Optional[Category]:
        stmt = select(Category).where(
            Category.id == category_id)
        result = (await self.session.execute(stmt)).scalar_one_or_none()
        if result:
            return

        raise ValueError(f'Категории с ID == {category_id} не существует!')

    async def get_all_categories(self, limit: int = None) -> [Category]:
        stmt = select(Category)
        if limit is not None:
            stmt = stmt.limit(limit)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_child_categories(self, parent_id: int) -> [Category]:
        """
        Возвращает список дочерних категорий для указанной родительской категории.
        :param parent_id: ID родительской категории.
        :return: Список дочерних категорий.
        """
        stmt = select(Category).where(
            Category.parent_id == parent_id
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def update_category(self, category_id: int, **data: dict) -> bool:
        # """
        # Обновляет данные категории.
        # :param category_id: ID категории.
        # :param name: Новое название категории (опционально).
        # :param parent_id: Новый ID родительской категории (опционально).
        # :return: Обновлённая категория или None, если категория не найдена.
        # """
        result = await self.get_category_by_id(category_id)
        if not result:
            raise ValueError('Категория не найдена!')

        allowed_fields = {
            "name",
            "parent_id"
        }
        update_data = {k: v for k, v in data.items() if k in allowed_fields}

        if not update_data:
            raise ValueError("Нет полей для обновления")

        stmt = (
            update(Category)
            .where(Category.id == category_id)
            .values(**update_data)
        )
        await self.session.execute(stmt)
        await self.session.commit()
        return True

    async def delete_category(self, category_id: int) -> bool:
        """
        Удаляет категорию по её ID.
        :param category_id: ID категории.
        :return: True, если категория удалена, иначе False.
        """
        category = await self.get_category_by_id(category_id)
        if not category:
            return False

        stmt = delete(Category).where(Category.id == category_id)

        await self.session.execute(stmt)
        await self.session.commit()
        return True
