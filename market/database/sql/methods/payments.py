from .include import Payment, select, update, insert, BaseDatabaseDep, PaymentStatus, PaymentCreate, Optional


class PaymentService(BaseDatabaseDep):
    async def create_payment(self, payment: PaymentCreate) -> int:
        stmt = insert(Payment).values(
            order_id=payment.order_id,
            amount=payment.amount,
            payment_method=payment.payment_method,
            transaction_id=payment.transaction_id
        )
        payment_id: int = (await self.session.execute(stmt)).scalar()
        await self.session.commit()
        return payment_id

    async def get_payment_by_id(self, payment_id: int) -> Optional[Payment]:
        stmt = select(Payment).where(
            Payment.id == payment_id
        )
        return (await self.session.execute(stmt)).scalar_one_or_none()

    async def update_payment_status(self, payment_id: int, status: PaymentStatus) -> bool:
        if await self.get_payment_by_id(payment_id):
            stmt = (
                update(Payment)
                .where(Payment.id == payment_id)
                .values(
                    status=status
                )
            )
            await self.session.execute(stmt)
            await self.session.commit()

            return True
        return False