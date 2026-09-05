from src.schemas.menu import MenuCreate, MenuUpdate
from src.db_models.menu import Menu
from src.schemas.user import UserCreate
from src.db_models.user import User
from src.db_models.menu_item import MenuItem
from src.schemas.menu_item import MenuItemCreate, MenuItemUpdate


class Mapper:

    @staticmethod
    def map(self, user_data: UserCreate) -> User:
        user = User(
            full_name=user_data.full_name,
            email=user_data.email,
            password=user_data.password,
            is_active=user_data.is_active,
        )
        return user

    @staticmethod
    def map_to_menu_item(item: MenuItemCreate) -> MenuItem:
        menu_item = MenuItem(
            name=item.name,
            price=item.price,
            category=item.category,
            description=item.description,
            menu_id=item.menu_id
        )
        return menu_item

    @staticmethod
    def map_to_update_menu_item(existing_item: MenuItem, item: MenuItemUpdate) -> MenuItem:

        if item.name is not None:
            existing_item.name = item.name

        if item.price is not None:
            existing_item.price = item.price

        if item.category is not None:
            existing_item.category = item.category

        if item.description is not None:
            existing_item.description = item.description

        return existing_item

    @staticmethod
    def map_to_menu(menu: MenuCreate) -> Menu:
        menu = Menu(
            name=menu.name,
            description=menu.description
        )
        return menu

    @staticmethod
    def map_to_update_menu(existing_menu: Menu, menu: MenuUpdate) -> Menu:
        if menu.name is not None:
            existing_menu.name = menu.name

        if menu.description is not None:
            existing_menu.description = menu.description

        return existing_menu

