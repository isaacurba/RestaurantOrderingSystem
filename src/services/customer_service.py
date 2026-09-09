from abc import ABC, abstractmethod

from src.db_models.menu_item import MenuItem
from src.db_models.order import Order
from src.db_models.user import User


class CustomerService(ABC):

    @abstractmethod
    def browse_menu(self, user: User) -> list[MenuItem]:
        pass

    @abstractmethod
    def view_menu_item_details(self, user: User, menu_item_id: int) -> MenuItem:
        pass

    @abstractmethod
    def add_item_to_order(self, user: User, menu_item_id: int, quantity: int) -> None:
        pass

    @abstractmethod
    def view_order(self, user: User) -> dict:
        pass

    @abstractmethod
    def place_order(self, user: User, address: str) -> Order:
        pass

    @abstractmethod
    def track_order(self, user: User, order_id: int) -> Order:
        pass

    @abstractmethod
    def cancel_order(self, user: User, order_id: int) -> None:
        pass
