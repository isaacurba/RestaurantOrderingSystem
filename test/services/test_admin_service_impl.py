import pytest

from database import SessionLocal
from src.services import admin_service
from src.repositories.menu_repository_impl import MenuRepositoryImpl
from src.exceptions.duplicate_menu_exception import DuplicateMenuException
from src.schemas.menu import MenuCreate, MenuUpdate
from src.db_models.menu import Menu
from src.db_models.menu_item import MenuItem
from src.db_models.user import User
from src.exceptions.duplicate_menu_item_exception import DuplicateMenuItemException
from src.exceptions.menu_item_not_found_exception import MenuItemNotFoundException
from src.exceptions.forbidden_exception import ForbiddenException
from src.models.category import Category
from src.models.user_role import UserRole
from src.repositories.menu_item_repository_impl import MenuItemRepositoryImpl
from src.schemas.menu_item import MenuItemCreate, MenuItemUpdate
from src.services.admin_service_impl import AdminServiceImpl


class TestAdminServiceImpl:

    @pytest.fixture
    def session(self):
        session = SessionLocal()

        yield session

        session.rollback()
        session.query(MenuItem).delete()
        session.query(Menu).delete()
        session.commit()
        session.close()

    @pytest.fixture
    def menu_repository(self, session):
        return MenuRepositoryImpl(session)

    @pytest.fixture
    def menu_item_repository(self, session):
        return MenuItemRepositoryImpl(session)

    @pytest.fixture
    def service(self, menu_repository, menu_item_repository):
        return AdminServiceImpl(
            menu_repository,
            menu_item_repository
        )

    @pytest.fixture
    def admin(self):
        return User(
            full_name="Admin User",
            email="admin@test.com",
            password="password",
            role=UserRole.ADMIN,
            is_active=True
        )

    @pytest.fixture
    def customer(self):
        return User(
            full_name="Customer User",
            email="customer@test.com",
            password="password",
            role=UserRole.CUSTOMER,
            is_active=True
        )

    @pytest.fixture
    def menu(self, session):
        menu = Menu(
            name="Lunch Menu",
            description="Menu for lunch meals"
        )

        session.add(menu)
        session.commit()
        session.refresh(menu)

        return menu

    @pytest.fixture
    def menu_create(self, session):
        return MenuCreate(
            name="Dinner Menu",
            description="Menu for dinner meals"
        )

    @pytest.fixture
    def menu_item(self, menu):
        return MenuItemCreate(
            name="Eba",
            price=200,
            category=Category.SWALLOW,
            description="two wraps of eba with fine egusi soup",
            menu_id=menu.id
        )

    def test_admin_can_create_menu(self, service, admin, menu_create):
        result = service.create_menu(admin, menu_create)

        assert result.name == "Dinner Menu"
        assert result.description == "Menu for dinner meals"

    def test_customer_cannot_create_menu(self, service, customer, menu_create):
        with pytest.raises(ForbiddenException):
            service.create_menu(customer, menu_create)

    def test_admin_cannot_create_duplicate_menu(self, service, admin, menu_create):
        service.create_menu(admin, menu_create)
        with pytest.raises(DuplicateMenuException):
            service.create_menu(admin, menu_create)

    def test_admin_can_update_menu(self, service, admin, menu_create):
        saved = service.create_menu(admin, menu_create)
        update = MenuUpdate(
            name="Break fast Menu",
            description="our wonderful breakfast alacha"
        )
        result = service.update_menu(admin, saved.id, update)

        assert result.name == "Break fast Menu"
        assert result.description == "our wonderful breakfast alacha"
        assert result.id == saved.id

    def test_customer_cannot_update_menu(self, service, customer, menu_create, admin):
        saved = service.create_menu(admin, menu_create)
        update = MenuUpdate(
            name="Break fast Menu",
            description="our wonderful breakfast alacha"
        )
        with pytest.raises(ForbiddenException):
            service.update_menu(customer, saved.id, update)

    def test_admin_can_remove_menu(self, service, admin, menu_create):
        saved = service.create_menu(admin, menu_create)
        service.remove_menu(admin, saved.id)

        assert service.menu_repository.find_by_id(saved.id) is None

    def test_customer_cannot_remove_menu(self, service, customer, menu_create, admin):
        saved = service.create_menu(admin, menu_create)
        with pytest.raises(ForbiddenException):
            service.remove_item(customer, saved.id)

    def test_add_menu_item(self, service, admin, menu_item):
        result = service.add_menu_item(admin, menu_item)

        assert result.name == "Eba"
        assert result.price == 200
        assert result.category == Category.SWALLOW
        assert result.description == "two wraps of eba with fine egusi soup"
        assert result.menu_id == menu_item.menu_id

    def test_customer_cannot_add_menu_item(self, service, customer,menu_item):
        with pytest.raises(ForbiddenException):
            service.add_menu_item(customer, menu_item)

    def test_to_add_duplicate_menu_item(self, service, admin,menu_item):
        service.add_menu_item(admin, menu_item)

        with pytest.raises(DuplicateMenuItemException):
            service.add_menu_item(admin, menu_item)

    def test_to_remove_menu_item(self, service, admin,menu_item):
        saved = service.add_menu_item(admin, menu_item)
        service.remove_item(admin, saved.id)

        assert service.menu_item_repository.find_by_id(saved.id) is None

    def test_customer_cannot_remove_menu_item(self, service, customer, admin, menu_item):
        saved = service.add_menu_item(admin, menu_item)

        with pytest.raises(ForbiddenException):
            service.remove_item(customer, saved.id)

    def test_update_menu_item(self,service,admin,menu_item):
        saved = service.add_menu_item(admin, menu_item)

        update = MenuItemUpdate(
            name="Amala",
            price=500,
            category=Category.SWALLOW,
            description="Amala with ewedu and gbegiri"
        )

        result = service.update_item(admin, saved.id, update)

        assert result.id == saved.id
        assert result.name == "Amala"
        assert result.price == 500
        assert result.category == Category.SWALLOW
        assert result.description == "Amala with ewedu and gbegiri"
        assert result.menu_id == saved.menu_id

    def test_customer_cannot_update_menu_item(self,service, customer, admin, menu_item):
        saved = service.add_menu_item(admin, menu_item)
        update = MenuItemUpdate(
            name="Amala",
            price=500
        )

        with pytest.raises(ForbiddenException):
            service.update_item(customer, saved.id, update)

    def test_update_non_existing_menu_item(self, service,admin):
        update = MenuItemUpdate(
            name="Amala",
            price=500
        )

        with pytest.raises(MenuItemNotFoundException):
            service.update_item(admin, 999999, update)