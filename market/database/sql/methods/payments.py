from market.database.sql.models import Payment, PaymentStatus


class PaymentService:
    @staticmethod
    def create_payment(session, order_id: int, amount: float, payment_method: str, transaction_id: str) -> Payment:
        """
        Создание платежа.
        """
        payment = Payment(
            order_id=order_id,
            amount=amount,
            payment_method=payment_method,
            transaction_id=transaction_id
        )
        session.add(payment)
        session.commit()
        return payment

    @staticmethod
    def update_payment_status(session, payment_id: int, status: PaymentStatus) -> Payment:
        """
        Обновление статуса платежа.
        """
        payment = session.query(Payment).filter(Payment.id == payment_id).first()
        if payment:
            payment.status = status
            session.commit()
        return payment