from sqlalchemy import select

from src.db_models.menu import Menu
from src.repositories.menu_repository import MenuRepository


class MenuRepositoryImpl(MenuRepository):

    def __init__(self, session):
        self.session = session

    def save(self, menu: Menu) -> Menu:
        self.session.add(menu)
        self.session.commit()
        self.session.refresh(menu)
        return menu

    def find_by_id(self, menu_id: int) -> Menu | None:
        return self.session.get(Menu, menu_id)

    def find_by_name(self, name: str) -> Menu | None:
        statement = select(Menu).where(Menu.name == name)
        return self.session.scalar(statement)

    def find_all(self) -> list[Menu]:
        statement = select(Menu)
        return list(self.session.scalars(statement).all())

    def delete(self, menu_id: int) -> None:
        menu = self.session.get(Menu, menu_id)

        if menu is not None:
            self.session.delete(menu)
            self.session.commit()