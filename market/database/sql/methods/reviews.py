from market.database.sql.models import Review


class ReviewService:
    @staticmethod
    def create_review(session, user_id: int, product_id: int, rating: int, comment: str) -> Review:
        """
        Создание отзыва.
        """
        review = Review(
            user_id=user_id,
            product_id=product_id,
            rating=rating,
            comment=comment
        )
        session.add(review)
        session.commit()
        return review

    @staticmethod
    def get_reviews_by_product(session, product_id: int) -> list[Review]:
        """
        Получение всех отзывов для продукта.
        """
        return session.query(Review).filter(Review.product_id == product_id).all()