from dataclasses import dataclass, field


@dataclass(slots=True)
class CustomerSubscriber:
    customer_id: str
    notifications: list[str] = field(default_factory=list)

    def notify_location(self, order_id: str, location: str) -> None:
        self.notifications.append(f"{order_id}:{location}")