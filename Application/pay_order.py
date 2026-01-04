from abc import ABC, abstractmethod
from domain.order import Order, Money
from dataclasses import dataclass


class OrderRepository(ABC):
    @abstractmethod
    def get(self, order_id: str) -> Order: pass
    @abstractmethod
    def save(self, order: Order) -> None: pass


class PaymentGateway(ABC):
    @abstractmethod
    def charge(self, order_id: str, amount: Money) -> str: pass


@dataclass
class PayOrderUseCase:
    orders: OrderRepository
    payment: PaymentGateway

    def execute(self, order_id: str) -> dict:
        order = self.orders.get(order_id)
        order.pay()
        transaction_id = self.payment.charge(order_id, order.total())
        self.orders.save(order)
        return {"success": True, "transaction_id": transaction_id}
