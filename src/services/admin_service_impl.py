from src.exceptions.menu_not_found_exception import MenuNotFoundException
from src.exceptions.duplicate_menu_exception import DuplicateMenuException
from schemas.menu import MenuUpdate, MenuResponse, MenuCreate
from src.exceptions.menu_item_not_found_exception import MenuItemNotFoundException
from src.exceptions.duplicate_menu_item_exception import DuplicateMenuItemException
from src.exceptions.forbidden_exception import ForbiddenException
from src.db_models.menu_item import MenuItem
from src.db_models.user import User
from src.models.user_role import UserRole
from src.schemas.menu_item import MenuItemResponse, MenuItemCreate, MenuItemUpdate
from src.services.admin_service import AdminService
from src.utils.mapper import Mapper


class AdminServiceImpl(AdminService):

    def __init__(self, menu_repository, menu_item_repository):
        self.menu_item_repository = menu_item_repository
        self.menu_repository = menu_repository

    def create_menu(self, user: User, menu: MenuCreate) -> MenuResponse:
        if user.role != UserRole.ADMIN or not user.is_active:
            raise ForbiddenException("Only active admins can perform this action")

        existing_menu = self.menu_repository.find_by_name(menu.name)

        if existing_menu is not None:
            raise DuplicateMenuException(f"Menu with name {menu.name} already exists")

        new_menu = Mapper.map_to_menu(menu)
        saved_menu = self.menu_repository.save(new_menu)
        return MenuResponse.model_validate(saved_menu)

    def update_menu(self, user: User, menu_id: int, menu: MenuUpdate) -> MenuResponse:
        if user.role != UserRole.ADMIN or not user.is_active:
            raise ForbiddenException("Only active admins can perform this action")
        existing_menu = self.menu_repository.find_by_id(menu_id)
        if existing_menu is None:
            raise MenuNotFoundException(f"Menu with id {menu_id } not found")

        updated_menu = Mapper.map_to_update_menu(existing_menu, menu)
        saved_menu = self.menu_repository.save(updated_menu)
        return MenuResponse.model_validate(saved_menu)

    def remove_menu(self, user: User, menu_id: int) -> None:
        if user.role != UserRole.ADMIN or not user.is_active:
            raise ForbiddenException("Only active admins can perform this action")
        existing_menu = self.menu_repository.find_by_id(menu_id)
        if existing_menu is None:
            raise MenuNotFoundException(f"Menu with id {menu_id} not found")
        self.menu_repository.delete(existing_menu.id)

    def add_menu_item(self,user: User,item: MenuItemCreate) -> MenuItemResponse:

        if user.role != UserRole.ADMIN or not user.is_active:
            raise ForbiddenException("Only active admins can create menu item")
        existing_menu_item = self.menu_item_repository.find_by_name(item.name)

        if existing_menu_item is not None:
            raise DuplicateMenuItemException(f"Menu item with name {item.name} already exists")
        menu_item = Mapper.map_to_menu_item(item)
        saved_item = self.menu_item_repository.save(menu_item)

        return MenuItemResponse.model_validate(saved_item)

    def remove_item(self, user: User, item_id: int) -> None:

        if user.role != UserRole.ADMIN or not user.is_active:
            raise ForbiddenException("Only active admins can remove menu item")
        existing_item = self.menu_item_repository.find_by_id(item_id)

        if existing_item is None:
            raise MenuItemNotFoundException(f"Menu item with id {item_id} not found")

        self.menu_item_repository.delete(item_id)

    def update_item(self, user: User, item_id: int, item: MenuItemUpdate) -> MenuItemResponse:

        if user.role != UserRole.ADMIN or not user.is_active:
            raise ForbiddenException("Only active admins can update menu item")

        existing_item = self.menu_item_repository.find_by_id(item_id)
        if existing_item is None:
            raise MenuItemNotFoundException(f"Menu item with id {item_id} not found")

        updated_item = Mapper.map_to_update_menu_item(existing_item, item)
        saved_item = self.menu_item_repository.save(updated_item)

        return MenuItemResponse.model_validate(saved_item)