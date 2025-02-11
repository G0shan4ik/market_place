from market.database.sql.models import OrderItem, OrderStatus, Order


class OrderService:
    @staticmethod
    def create_order(session, buyer_id: int, total_amount: float, shipping_address_id: int) -> Order:
        """
        Создание нового заказа.
        """
        order = Order(
            buyer_id=buyer_id,
            total_amount=total_amount,
            shipping_address_id=shipping_address_id
        )
        session.add(order)
        session.commit()
        return order

    @staticmethod
    def get_order_by_id(session, order_id: int) -> Order:
        """
        Получение заказа по ID.
        """
        return session.query(Order).filter(Order.id == order_id).first()

    @staticmethod
    def update_order_status(session, order_id: int, status: OrderStatus) -> Order:
        """
        Обновление статуса заказа.
        """
        order = session.query(Order).filter(Order.id == order_id).first()
        if order:
            order.status = status
            session.commit()
        return order

    @staticmethod
    def add_order_item(session, order_id: int, product_id: int, quantity: int, price_at_purchase: float) -> OrderItem:
        """
        Добавление товара в заказ.
        """
        order_item = OrderItem(
            order_id=order_id,
            product_id=product_id,
            quantity=quantity,
            price_at_purchase=price_at_purchase
        )
        session.add(order_item)
        session.commit()
        return order_item