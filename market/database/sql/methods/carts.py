from datetime import datetime
from typing import Optional

from .include import Cart, CartItem, CartItemRemove, CartItemsIds, select, delete, update, insert, BaseDatabaseDep, CartItemUpdate


class CartService(BaseDatabaseDep):
    async def create_cart(self, user_id: int) -> int:
        stmt = insert(Cart).values(user_id=user_id).returning(Cart.id)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.scalar()

    async def get_cart_by_id(self, cart_id: int) -> Optional[Cart]:
        stmt = select(Cart).where(Cart.id == cart_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def update_cart(self, cart_id: int) -> bool:
        cart = await self.get_cart_by_id(cart_id)
        if cart:
            stmt = update(Cart).where(Cart.id == cart_id).values(updated_at=datetime.utcnow())
            await self.session.execute(stmt)
            await self.session.commit()
            return True
        return False

    async def delete_cart(self, cart_id: int) -> bool:
        cart = await self.get_cart_by_id(cart_id)
        if cart:
            stmt = delete(Cart).where(Cart.id == cart_id)
            await self.session.execute(stmt)
            await self.session.commit()
            return True
        return False

    async def create_or_update_item(self, cart_item: CartItemUpdate) -> int:
        stmt = select(CartItem).where(
            (CartItem.cart_id == cart_item.cart_id) & (CartItem.product_id == cart_item.product_id)
        )
        result = await self.session.execute(stmt)
        item = result.scalar_one_or_none()

        if item:
            stmt = update(CartItem).where(
                (CartItem.cart_id == cart_item.cart_id) & (CartItem.product_id == cart_item.product_id)
            ).values(quantity=item.quantity + cart_item.quantity).returning(CartItem.id)
        else:
            stmt = insert(CartItem).values(
                cart_id=cart_item.cart_id,
                product_id=cart_item.product_id,
                quantity=cart_item.quantity
            ).returning(CartItem.id)

        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.scalar_one_or_none()

    async def get_item_by_id(self, item_id: int) -> Optional[CartItem]:
        stmt = select(CartItem).where(CartItem.id == item_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_items(self, cart_item: CartItemsIds) -> [CartItem]:
        stmt = select(CartItem)
        if cart_item.cart_id:
            stmt = stmt.where(CartItem.cart_id == cart_item.cart_id)
        if cart_item.product_id:
            stmt = stmt.where(CartItem.product_id == cart_item.product_id)

        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def delete_item(self, cart_item: CartItemRemove) -> bool:
        stmt = None
        if cart_item.product_id:
            stmt = delete(CartItem).where(
                (CartItem.cart_id == cart_item.cart_id) & (CartItem.product_id == cart_item.product_id)
            )
        elif cart_item.item_id:
            stmt = delete(CartItem).where(CartItem.id == cart_item.item_id)

        if stmt:
            await self.session.execute(stmt)
            await self.session.commit()
            return True
        return False
