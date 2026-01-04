import pytest
from decimal import Decimal
from domain.order import Order, OrderLine, Money
from infrastructure.repository import InMemoryOrderRepository
from infrastructure.payment import FakePaymentGateway
from application.pay_order import PayOrderUseCase


def test_successful_payment():
    # Arrange
    repo = InMemoryOrderRepository()
    payment = FakePaymentGateway()
    use_case = PayOrderUseCase(repo, payment)
    
    order = Order(id="1", customer_id="cust1")
    order.add_line(OrderLine("p1", 2, Money(Decimal("10.0"))))
    repo.save(order)
    
    # Act
    result = use_case.execute("1")
    
    # Assert
    assert result["success"]
    assert repo.get("1").status.name == "PAID"


def test_cannot_pay_empty_order():
    repo = InMemoryOrderRepository()
    payment = FakePaymentGateway()
    use_case = PayOrderUseCase(repo, payment)
    
    empty_order = Order(id="2", customer_id="cust1")
    repo.save(empty_order)
    
    with pytest.raises(ValueError, match="Cannot pay empty order"):
        use_case.execute("2")


def test_cannot_pay_twice():
    repo = InMemoryOrderRepository()
    payment = FakePaymentGateway()
    use_case = PayOrderUseCase(repo, payment)
    
    order = Order(id="3", customer_id="cust1")
    order.add_line(OrderLine("p1", 1, Money(Decimal("10.0"))))
    repo.save(order)
    
    # Первый раз успешно
    use_case.execute("3")
    
    # Второй раз ошибка
    with pytest.raises(ValueError, match="Order already paid"):
        use_case.execute("3")


def test_cannot_modify_after_payment():
    order = Order(id="4", customer_id="cust1")
    order.add_line(OrderLine("p1", 1, Money(Decimal("10.0"))))
    order.pay()
    
    with pytest.raises(ValueError, match="Cannot modify paid order"):
        order.add_line(OrderLine("p2", 1, Money(Decimal("20.0"))))


def test_total_calculation():
    order = Order(id="5", customer_id="cust1")
    order.add_line(OrderLine("p1", 2, Money(Decimal("15.0"))))
    order.add_line(OrderLine("p2", 1, Money(Decimal("30.0"))))
    
    assert order.total().amount == Decimal("60.0")
