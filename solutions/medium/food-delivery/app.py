from models.order import Order
from models.subscriber import CustomerSubscriber
from services.delivery_service import DeliveryService


def main() -> None:
    service = DeliveryService()
    order = Order(order_id="O1", customer_id="C1")
    subscriber = CustomerSubscriber(customer_id="C1")

    service.create_order(order)
    service.subscribe(order.order_id, subscriber)
    print(service.advance_status(order.order_id))
    print(service.advance_status(order.order_id))
    print(service.advance_status(order.order_id))
    print(service.push_location(order.order_id, "12.97,77.59"))
    print(subscriber.notifications)


if __name__ == "__main__":
    main()