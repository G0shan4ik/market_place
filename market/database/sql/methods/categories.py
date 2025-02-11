from market.database.sql.models import Category


class CategoryService:
    @staticmethod
    def create_category(session, name: str, parent_id: int | None = None) -> Category:
        """
        Создание категории.
        """
        category = Category(name=name, parent_id=parent_id)
        session.add(category)
        session.commit()
        return category

    @staticmethod
    def get_category_by_id(session, category_id: int) -> Category:
        """
        Получение категории по ID.
        """
        return session.query(Category).filter(Category.id == category_id).first()

    @staticmethod
    def get_child_categories(session, parent_id: int) -> list[Category]:
        """
        Получение дочерних категорий.
        """
        return session.query(Category).filter(Category.parent_id == parent_id).all()