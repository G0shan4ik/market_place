from .include import Product, ProductCreate, select, delete, update, insert, BaseDatabaseDep, Optional


class ProductService(BaseDatabaseDep):
    async def create_product(self, product_: ProductCreate) -> int:
        stmt = insert(Product).values(
            name = product_.name,
            description = product_.description,
            price = product_.price,
            stock = product_.stock,
            seller_id = product_.seller_id,
            category_id = product_.category_id
        ).returning(Product.id)

        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.scalar()

    async def get_product_by_id(self, product_id: int) -> Optional[Product]:
        stmt = select(Product).where(
            Product.id == product_id
        )
        return (await self.session.execute(stmt)).scalar_one_or_none()

    async def update_product(self, product_id: int, data: dict) -> bool:
        product = self.get_product_by_id(product_id=product_id)
        if product:
            allowed_fields = {
                "name",
                "description",
                "price",
                "stock"
            }
            update_data = {k: v for k, v in data.items() if k in allowed_fields}

            if not update_data:
                raise ValueError("Нет полей для обновления")

            stmt = (
                update(Product)
                .where(Product.id == product_id)
                .values(**update_data)
            )
            await self.session.execute(stmt)
            await self.session.commit()

            return True
        raise ValueError('Продукт не найден!')

    async def delete_product(self, product_id: int) -> bool:
        product = self.get_product_by_id(product_id)
        if product:
            stmt = delete(Product).where(Product.id == product_id)

            await self.session.execute(stmt)
            await self.session.commit()
            return True
        return False

    async def get_products_by_category(self, category_id: int) -> [Product]:
        stmt = select(Product).filter(
            Product.category_id == category_id
        )

        result = await self.session.execute(stmt)
        return result.scalars().all()