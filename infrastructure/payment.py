from application.pay_order import PaymentGateway
from domain.order import Money


class FakePaymentGateway(PaymentGateway):
    def charge(self, order_id: str, amount: Money) -> str:
        return f"txn_{order_id[:8]}"
