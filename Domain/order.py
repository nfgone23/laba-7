from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from decimal import Decimal
from typing import List


class OrderStatus(Enum):
    CREATED = "created"
    PAID = "paid"


@dataclass
class Money:
    amount: Decimal
    currency: str = "USD"

@dataclass
class OrderLine:
    product_id: str
    quantity: int
    price: Money

@dataclass
class Order:
    id: str
    customer_id: str
    lines: List[OrderLine] = field(default_factory=list)
    status: OrderStatus = OrderStatus.CREATED
    paid_at: datetime = None

    def total(self) -> Money:
        if not self.lines:
            return Money(Decimal('0'))
        total_amount = sum(line.price.amount * line.quantity 
                          for line in self.lines)
        return Money(total_amount, self.lines[0].price.currency)

    def pay(self) -> None:
        if not self.lines:
            raise ValueError("Cannot pay empty order")
        if self.status == OrderStatus.PAID:
            raise ValueError("Order already paid")
        self.status = OrderStatus.PAID
        self.paid_at = datetime.now()

    def add_line(self, line: OrderLine) -> None:
        if self.status == OrderStatus.PAID:
            raise ValueError("Cannot modify paid order")
        self.lines.append(line)
