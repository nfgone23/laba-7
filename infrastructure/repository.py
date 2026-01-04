from typing import Dict
from application.pay_order import OrderRepository
from domain.order import Order


class InMemoryOrderRepository(OrderRepository):
    def __init__(self):
        self.storage: Dict[str, Order] = {}

    def get(self, order_id: str) -> Order:
        return self.storage[order_id]

    def save(self, order: Order) -> None:
        self.storage[order.id] = order
