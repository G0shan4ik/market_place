from collections import defaultdict

from .include import Order, OrderItem, select, delete, OrderCreate, update, insert, BaseDatabaseDep, OrderStatus, Optional


class OrderService(BaseDatabaseDep):
    async def create_order(self, order_: OrderCreate) -> int:
        stmt = insert(Order).values(
            buyer_id=order_.buyer_id,
            total_amount=order_.total_amount,
            shipping_address_id=order_.shipping_address_id
        ).returning(Order.id)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.scalar()

    async def get_order_by_id(self, order_id: int) -> Order:
        stmt = select(Order).where(
            Order.id == order_id
        )
        return (await self.session.execute(stmt)).scalar_one_or_none()

    async def update_order_status(self, order_id: int, status: OrderStatus) -> bool:
        order = self.get_order_by_id(order_id=order_id)
        if order:
            stmt = update(Order).where(Order.id == order_id).values(
                status = status
            )
            await self.session.execute(stmt)
            await self.session.commit()
            return True
        raise ValueError('Ордер не найден!')

    async def delete_order(self, order_id: int) -> bool:
        order = await self.get_order_by_id(order_id)
        if not order:
            return False

        await self.session.execute(delete(Order).where(Order.id == order_id))
        await self.session.commit()
        return True

    async def add_order_item(
            self,
            order_id: int,
            product_id: int,
            quantity: int,
            price_at_purchase: float
    ) -> int:
        if await self.get_order_by_id(order_id):
            stmt = insert(OrderItem).values(
                quantity=quantity,
                price_at_purchase=price_at_purchase,
                order_id=order_id,
                product_id=product_id
            ).returning(OrderItem.id)

            result = await self.session.execute(stmt)
            await self.session.commit()
            return result.scalar()
        raise ValueError('Ордер не найден!')

    async def get_order_items(self, order_id: int) -> [OrderItem]:
        result = await self.session.execute(
            select(OrderItem).where(OrderItem.order_id == order_id)
        )
        return result.scalars().all()

    async def get_item_id(self, order_id: int) -> Order:
        stmt = select(Order).where(
            Order.id == order_id
        )
        return (await self.session.execute(stmt)).scalar_one_or_none()

    async def update_order_item_quantity(self, item_id: int, quantity: int) -> bool:
        if not await self.get_item_id(item_id):
            return False

        await self.session.execute(
            update(OrderItem).values(quantity=quantity)
        )
        await self.session.commit()
        return True

    async def delete_order_item(self, item_id: int) -> bool:
        if not await self.get_item_id(item_id):
            return False

        await self.session.execute(delete(OrderItem).where(OrderItem.id == item_id))
        await self.session.commit()
        return True

    async def get_orders_by_buyer(self, buyer_id: int) -> Optional[list[Order], dict[int, [OrderItem]]]:
        """
        Returns:
            - A list of the buyers orders.
            - Dictionary of order elements, where the key is the order ID.
        """
        orders_result = await self.session.execute(
            select(Order).where(Order.buyer_id == buyer_id)
        )
        orders: [Order] = orders_result.scalars().all()

        if not orders:
            return None

        order_ids = [order.id for order in orders]
        items_result = await self.session.execute(
            select(OrderItem).where(OrderItem.order_id.in_(order_ids))
        )
        items = items_result.scalars().all()

        items_by_order = defaultdict(list)
        for item in items:
            items_by_order[item.order_id].append(item)

        return [orders, items_by_order]