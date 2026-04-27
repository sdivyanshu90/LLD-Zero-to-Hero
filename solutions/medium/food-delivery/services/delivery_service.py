from __future__ import annotations

from dataclasses import dataclass, field

from models.order import Order, OrderStatus
from models.subscriber import CustomerSubscriber


@dataclass(slots=True)
class DeliveryService:
    orders: dict[str, Order] = field(default_factory=dict)
    subscribers: dict[str, list[CustomerSubscriber]] = field(default_factory=dict)

    _transitions: dict[OrderStatus, OrderStatus] = field(
        default_factory=lambda: {
            OrderStatus.CREATED: OrderStatus.ACCEPTED,
            OrderStatus.ACCEPTED: OrderStatus.PREPARING,
            OrderStatus.PREPARING: OrderStatus.OUT_FOR_DELIVERY,
            OrderStatus.OUT_FOR_DELIVERY: OrderStatus.DELIVERED,
        },
        init=False,
        repr=False,
    )

    def create_order(self, order: Order) -> None:
        self.orders[order.order_id] = order

    def subscribe(self, order_id: str, subscriber: CustomerSubscriber) -> None:
        order = self._get_order(order_id)
        if subscriber.customer_id != order.customer_id:
            raise ValueError("Subscriber does not match the order customer")
        self.subscribers.setdefault(order_id, []).append(subscriber)

    def advance_status(self, order_id: str) -> str:
        order = self._get_order(order_id)
        next_status = self._transitions.get(order.status)
        if next_status is None:
            raise ValueError(f"No further transition allowed from {order.status.value}")
        order.status = next_status
        return f"{order_id} -> {order.status.value}"

    def push_location(self, order_id: str, location: str) -> str:
        order = self._get_order(order_id)
        if order.status is not OrderStatus.OUT_FOR_DELIVERY:
            raise ValueError("Location updates are only allowed while out for delivery")
        for subscriber in self.subscribers.get(order_id, []):
            subscriber.notify_location(order_id, location)
        return f"Pushed location for {order_id}"

    def _get_order(self, order_id: str) -> Order:
        order = self.orders.get(order_id)
        if order is None:
            raise ValueError(f"Unknown order {order_id}")
        return order