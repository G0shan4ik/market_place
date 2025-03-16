from collections import defaultdict

from .include import Order, OrderItem, OrderItemCreate, select, delete, OrderCreate, update, insert, BaseDatabaseDep, OrderStatus, Optional
from ..models import Address


class OrderService(BaseDatabaseDep):
    async def create_order(self, order_: OrderCreate) -> int:
        _stmt = select(Address).where(Address.id == order_.shipping_address_id)
        assert (await self.session.execute(_stmt)).scalar_one_or_none(), \
            f'Адреса с таким id не существует (shipping_address_id=={order_.shipping_address_id})'

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
        result = (await self.session.execute(stmt)).scalar_one_or_none()
        assert result, f"Ордера с таким id (order_id=={order_id}) не существует"

        return result

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

    async def add_order_item(self, order: OrderItemCreate) -> int:
        if await self.get_order_by_id(order.order_id):
            stmt = insert(OrderItem).values(
                quantity=order.quantity,
                price_at_purchase=order.price_at_purchase,
                order_id=order.order_id,
                product_id=order.product_id
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

    async def get_item_by_id(self, item_id: int) -> OrderItem:
        stmt = select(OrderItem).where(
            OrderItem.id == item_id
        )
        return (await self.session.execute(stmt)).scalar_one_or_none()

    async def update_order_item_quantity(self, item_id: int, quantity: int) -> bool:
        if not await self.get_item_by_id(item_id):
            return False

        await self.session.execute(
            update(OrderItem).values(quantity=quantity)
        )
        await self.session.commit()
        return True

    async def delete_order_item(self, item_id: int) -> bool:
        if not await self.get_item_by_id(item_id):
            return False

        await self.session.execute(delete(OrderItem).where(OrderItem.id == item_id))
        await self.session.commit()
        return True

    async def get_orders_by_buyer(self, buyer_id: int) -> Optional[dict]:
        """
        Returns dictionary with:
        - 'orders': list of buyer's orders
        - 'order_items': dictionary {order_id: list_of_items}

        Returns None if no orders found
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

        order_items: dict[int, list[OrderItem]] = defaultdict(list)
        for item in items:
            order_items[item.order_id].append(item)

        return {
            'orders': orders,
            'order_items': dict(order_items)
        }