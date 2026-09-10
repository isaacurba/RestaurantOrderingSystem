from sqlalchemy import select
from sqlalchemy.orm import joinedload

from src.db_models.order import Order
from src.db_models.order_item import OrderItem
from src.models.order_status import OrderStatus
from src.repositories.order_repository import OrderRepository


class OrderRepositoryImpl(OrderRepository):

    def __init__(self, session):
        self.session = session

    def save(self, order: Order) -> Order:
        self.session.add(order)
        self.session.commit()
        self.session.refresh(order)
        return order

    def save_order_item(self, order_item: OrderItem) -> OrderItem:
        self.session.add(order_item)
        self.session.commit()
        self.session.refresh(order_item)
        return order_item

    def find_by_id(self, order_id: int) -> Order | None:
        statement = (
            select(Order)
            .where(Order.id == order_id)
            .options(joinedload(Order.order_items))
        )
        return self.session.scalar(statement)

    def find_pending_by_user_id(self, user_id: int) -> Order | None:
        statement = (
            select(Order)
            .where(Order.user_id == user_id, Order.status == OrderStatus.PENDING)
            .options(joinedload(Order.order_items))
        )
        return self.session.scalar(statement)

    def delete(self, order_id: int) -> None:
        order = self.session.get(Order, order_id)

        if order is not None:
            self.session.delete(order)
            self.session.commit()
