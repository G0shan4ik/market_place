from .include import Review, select, delete, insert, BaseDatabaseDep, ReviewCreate, Optional


class ReviewService(BaseDatabaseDep):
    async def create_review(self, review: ReviewCreate) -> int:
        stmt = insert(Review).values(
            user_id=review.user_id,
            product_id=review.product_id,
            rating=review.rating,
            comment=review.comment
        ).returning(Review.id)

        review_id: int = (await self.session.execute(stmt)).scalar()
        await self.session.commit()

        return review_id

    async def get_review_by_id(self, review_id: int) -> Optional[Review]:
        stmt = select(Review).where(
            Review.id == review_id
        )
        return (await self.session.execute(stmt)).scalar_one_or_none()

    async def delete_review(self, review_id: int) -> bool:
        if await self.get_review_by_id(review_id):
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