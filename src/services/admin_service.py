from abc import ABC, abstractmethod

from schemas.menu import MenuCreate, MenuResponse, MenuUpdate
from src.db_models.user import User
from src.schemas.menu_item import MenuItemResponse, MenuItemCreate, MenuItemUpdate


class AdminService(ABC):

    @abstractmethod
    def create_menu(self, user: User, menu: MenuCreate) -> MenuResponse:
        pass

    @abstractmethod
    def update_menu(self, user: User, menu_id: int, menu: MenuUpdate) -> MenuResponse:
        pass

    @abstractmethod
    def remove_menu(self, user: User, menu_id: int) -> None:
        pass

    @abstractmethod
    def add_menu_item(self, user: User, item: MenuItemCreate) -> MenuItemResponse:
        pass

    @abstractmethod
    def remove_item(self, user: User, item_id: int) -> None:
        pass

    @abstractmethod
    def update_item(self, user: User, item_id: int, item: MenuItemUpdate) -> MenuItemResponse:
        pass