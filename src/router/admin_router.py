from src.schemas.menu_item import MenuItemResponse, MenuItemCreate, MenuItemUpdate
from src.utils.auth import get_current_user
from fastapi import APIRouter, Depends, status

from src.database import SessionLocal
from src.repositories.menu_item_repository_impl import MenuItemRepositoryImpl
from src.repositories.menu_repository_impl import MenuRepositoryImpl
from src.services.admin_service_impl import AdminServiceImpl
from src.controller.admin_service_controller import AdminServiceController
from src.schemas.menu import MenuCreate, MenuResponse, MenuUpdate
from src.db_models.user import User

router = APIRouter(prefix="/admin", tags=["Admin"])

def get_controller():
    session = SessionLocal()
    menu_repository = MenuRepositoryImpl(session)
    menu_item_repository = MenuItemRepositoryImpl(session)
    service = AdminServiceImpl(menu_repository, menu_item_repository)

    return AdminServiceController(service)

@router.post("/create_menu", response_model=MenuResponse, status_code=status.HTTP_201_CREATED)
def create_menu(menu_data: MenuCreate, user: User = Depends(get_current_user)):
    controller = get_controller()
    return controller.create_menu(user, menu_data)

@router.put("/update_menu", response_model=MenuResponse, status_code=status.HTTP_200_OK)
def update_menu(menu_id: int, menu_data: MenuUpdate, user: User = Depends(get_current_user)):
    controller = get_controller()
    return controller.update_menu(user, menu_id, menu_data)

@router.delete("/delete_menu", status_code=status.HTTP_204_NO_CONTENT)
def delete_menu(menu_id: int, user: User = Depends(get_current_user)):
    controller = get_controller()
    controller.delete_menu(user, menu_id)

@router.post("/create_menu_item", response_model=MenuItemResponse, status_code=status.HTTP_200_OK)
def create_menu_item(item: MenuItemCreate, user: User = Depends(get_current_user)):
    controller = get_controller()
    return controller.create_menu_item(user, item)

@router.put("/update_menu_item", response_model=MenuItemResponse, status_code=status.HTTP_200_OK)
def update_menu_item(menu_item_id: int, item: MenuItemUpdate, user: User = Depends(get_current_user)):
    controller = get_controller()
    return controller.update_menu_item(user, menu_item_id, item)

@router.delete("/delete_menu_item", status_code=status.HTTP_204_NO_CONTENT)
def delete_menu_item(menu_item_id: int, user: User = Depends(get_current_user)):
    controller = get_controller()
    controller.remove_menu_item(user, menu_item_id)
