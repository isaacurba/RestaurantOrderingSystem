from abc import ABC, abstractmethod

from src.db_models.order import Order
from src.db_models.order_item import OrderItem


class OrderRepository(ABC):

    @abstractmethod
    def save(self, order: Order) -> Order:
        pass

    @abstractmethod
    def save_order_item(self, order_item: OrderItem) -> OrderItem:
        pass

    @abstractmethod
    def find_by_id(self, order_id: int) -> Order | None:
        pass

    @abstractmethod
    def find_pending_by_user_id(self, user_id: int) -> Order | None:
        pass

    @abstractmethod
    def delete(self, order_id: int) -> None:
        pass
