from market.database.sql.models import CartItem


class CartService:
    @staticmethod
    def add_to_cart(session, cart_id: int, product_id: int, quantity: int = 1) -> CartItem:
        """
        Добавление товара в корзину.
        """
        cart_item = CartItem(
            cart_id=cart_id,
            product_id=product_id,
            quantity=quantity
        )
        session.add(cart_item)
        session.commit()
        return cart_item

    @staticmethod
    def remove_from_cart(session, cart_item_id: int) -> bool:
        """
        Удаление товара из корзины.
        """
        cart_item = session.query(CartItem).filter(CartItem.id == cart_item_id).first()
        if cart_item:
            session.delete(cart_item)
            session.commit()
            return True
        return False

    @staticmethod
    def get_cart_items(session, cart_id: int) -> list[CartItem]:
        """
        Получение всех товаров в корзине.
        """
        return session.query(CartItem).filter(CartItem.cart_id == cart_id).all()