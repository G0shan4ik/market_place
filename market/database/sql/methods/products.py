from market.database.sql.models import Product


class ProductService:
    @staticmethod
    def create_product(session, name: str, description: str, price: float, seller_id: int, category_id: int, stock: int = 0) -> Product:
        """
        Создание нового продукта.
        """
        product = Product(
            name=name,
            description=description,
            price=price,
            seller_id=seller_id,
            category_id=category_id,
            stock=stock
        )
        session.add(product)
        session.commit()
        return product

    @staticmethod
    def get_product_by_id(session, product_id: int) -> Product:
        """
        Получение продукта по ID.
        """
        return session.query(Product).filter(Product.id == product_id).first()

    @staticmethod
    def update_product(session, product_id: int, **kwargs) -> Product:
        """
        Обновление данных продукта.
        """
        product = session.query(Product).filter(Product.id == product_id).first()
        if product:
            for key, value in kwargs.items():
                setattr(product, key, value)
            session.commit()
        return product

    @staticmethod
    def delete_product(session, product_id: int) -> bool:
        """
        Удаление продукта по ID.
        """
        product = session.query(Product).filter(Product.id == product_id).first()
        if product:
            session.delete(product)
            session.commit()
            return True
        return False

    @staticmethod
    def get_products_by_category(session, category_id: int) -> list[Product]:
        """
        Получение всех продуктов в категории.
        """
        return session.query(Product).filter(Product.category_id == category_id).all()