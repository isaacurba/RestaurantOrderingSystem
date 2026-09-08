from src.schemas.menu_item import MenuItemCreate, MenuItemResponse, MenuItemUpdate
from src.schemas.menu import MenuCreate, MenuResponse, MenuUpdate
from src.db_models.user import User
from src.services.admin_service import AdminService


class AdminServiceController:

    def __init__(self, service: AdminService):
        self.service = service

    def create_menu(self, user: User, menu_data: MenuCreate) -> MenuResponse:
        return self.service.create_menu(user, menu_data)

    def update_menu(self, user: User, menu_id: int,menu_data: MenuUpdate) -> MenuResponse:
        return self.service.update_menu(user, menu_id, menu_data)

    def delete_menu(self, user: User, menu_id: int) -> None:
        self.service.remove_menu(user, menu_id)

    def create_menu_item(self, user: User, menu_data: MenuItemCreate) -> MenuItemResponse:
        return self.service.add_menu_item(user, menu_data)

    def update_menu_item(self, user: User, menu_item_id: int, menu_data: MenuItemUpdate) -> MenuItemResponse:
        return self.service.update_item(user, menu_item_id, menu_data)

    def remove_menu_item(self, user: User, menu_id: int) -> None:
        return self.service.remove_item(user, menu_id)