from dataclasses import dataclass
from enum import Enum


class OrderStatus(Enum):
    CREATED = "created"
    ACCEPTED = "accepted"
    PREPARING = "preparing"
    OUT_FOR_DELIVERY = "out_for_delivery"
    DELIVERED = "delivered"


@dataclass(slots=True)
class Order:
    order_id: str
    customer_id: str
    status: OrderStatus = OrderStatus.CREATED