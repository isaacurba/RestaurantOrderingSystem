from abc import ABC, abstractmethod

from src.db_models.menu import Menu


class MenuRepository(ABC):

    @abstractmethod
    def save(self, menu: Menu) -> Menu:
        pass

    @abstractmethod
    def find_by_id(self, menu_id: int) -> Menu | None:
        pass

    @abstractmethod
    def find_by_name(self, name: str) -> Menu | None:
        pass

    @abstractmethod
    def find_all(self) -> list[Menu]:
        pass

    @abstractmethod
    def delete(self, menu_id: int) -> None:
        pass