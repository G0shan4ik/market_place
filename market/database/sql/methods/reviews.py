from .include import Review, select, delete, insert, BaseDatabaseDep


class ReviewService(BaseDatabaseDep):
    async def create_review(self, user_id: int, product_id: int, rating: int, comment: str) -> int:
        stmt = insert(Review).values(
            user_id=user_id,
            product_id=product_id,
            rating=rating,
            comment=comment
        ).returning(Review.id)

        review_id: int = (await self.session.execute(stmt)).scalar()
        await self.session.commit()

        return review_id

    async def get_review_by_id(self, review_id: int):
        stmt = select(Review).where(
            Review.id == review_id
        )
        return (await self.session.execute(stmt)).scalar_one_or_none()

    async def delete_review(self, review_id: int):
        if self.get_review_by_id(review_id):
            stmt = delete(Review).where(
                Review.id == review_id
            )
            await self.session.execute(stmt)
            await self.session.commit()
            return True
        return False

    async def get_reviews_by_product(self, product_id: int) -> [Review]:
        stmt = select(Review).filter(
            Review.product_id == product_id
        )
        return (await self.session.execute(stmt)).scalars().all()