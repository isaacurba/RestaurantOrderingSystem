from src.db_models.menu_item import MenuItem
from src.db_models.order import Order
from src.db_models.order_item import OrderItem
from src.db_models.user import User
from src.exceptions.forbidden_exception import ForbiddenException
from src.exceptions.menu_item_not_found_exception import MenuItemNotFoundException
from src.exceptions.order_cancellation_exception import OrderCancellationException
from src.exceptions.order_not_found_exception import OrderNotFoundException
from src.models.order_status import OrderStatus
from src.models.user_role import UserRole
from src.services.customer_service import CustomerService


class CustomerServiceImpl(CustomerService):

    def __init__(self, menu_item_repository, order_repository):
        self.menu_item_repository = menu_item_repository
        self.order_repository = order_repository

    def _require_customer(self, user: User) -> None:
        if user.role != UserRole.CUSTOMER or not user.is_active:
            raise ForbiddenException("Only active customers can perform this action")

    def _get_or_create_pending_order(self, user: User) -> Order:
        order = self.order_repository.find_pending_by_user_id(user.id)
        if order is None:
            order = Order(
                user_id=user.id,
                total_amount=0.0,
                status=OrderStatus.PENDING,
            )
            order = self.order_repository.save(order)
        return order

    def _recalculate_total(self, order: Order) -> float:
        return sum(float(item.price) * item.quantity for item in order.order_items)

    def browse_menu(self, user: User) -> list[MenuItem]:
        self._require_customer(user)
        return self.menu_item_repository.find_all()

    def view_menu_item_details(self, user: User, menu_item_id: int) -> MenuItem:
        self._require_customer(user)
        item = self.menu_item_repository.find_by_id(menu_item_id)
        if item is None:
            raise MenuItemNotFoundException(
                f"Menu item with id {menu_item_id} not found"
            )
        return item

    def add_item_to_order(self, user: User, menu_item_id: int, quantity: int) -> None:
        self._require_customer(user)

        menu_item = self.menu_item_repository.find_by_id(menu_item_id)
        if menu_item is None:
            raise MenuItemNotFoundException(
                f"Menu item with id {menu_item_id} not found"
            )

        order = self._get_or_create_pending_order(user)

        existing_item = next(
            (oi for oi in order.order_items if oi.menu_item_id == menu_item_id),
            None,
        )

        if existing_item is not None:
            existing_item.quantity += quantity
            self.order_repository.save_order_item(existing_item)
        else:
            order_item = OrderItem(
                order_id=order.id,
                menu_item_id=menu_item_id,
                quantity=quantity,
                price=float(menu_item.price),
            )
            self.order_repository.save_order_item(order_item)
            order.order_items.append(order_item)

        order.total_amount = self._recalculate_total(order)
        self.order_repository.save(order)

    def view_order(self, user: User) -> Order:
        self._require_customer(user)

        order = self.order_repository.find_pending_by_user_id(user.id)
        if order is None:
            raise OrderNotFoundException(
                "No active order found. Add items to start an order."
            )
        return order

    def place_order(self, user: User, address: str) -> Order:
        self._require_customer(user)

        order = self.order_repository.find_pending_by_user_id(user.id)
        if order is None:
            raise OrderNotFoundException(
                "No active order found. Add items before placing an order."
            )

        if not order.order_items:
            raise ValueError("Cannot place an order that contains no items.")

        order.status = OrderStatus.CONFIRMED
        return self.order_repository.save(order)

    def track_order(self, user: User, order_id: int) -> Order:
        self._require_customer(user)

        order = self.order_repository.find_by_id(order_id)
        if order is None or order.user_id != user.id:
            raise OrderNotFoundException(
                f"Order with id {order_id} not found for this customer"
            )
        return order

    def cancel_order(self, user: User, order_id: int) -> None:
        self._require_customer(user)

        order = self.order_repository.find_by_id(order_id)
        if order is None or order.user_id != user.id:
            raise OrderNotFoundException(
                f"Order with id {order_id} not found for this customer"
            )

        cancellable_statuses = {OrderStatus.PENDING, OrderStatus.CONFIRMED}
        if order.status not in cancellable_statuses:
            raise OrderCancellationException(
                f"Order with id {order_id} cannot be cancelled "
                f"because it is already {order.status.value}"
            )

        order.status = OrderStatus.CANCELLED
        self.order_repository.save(order)
