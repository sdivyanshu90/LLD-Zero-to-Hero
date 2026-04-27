from dataclasses import dataclass, field


@dataclass(slots=True)
class Member:
    member_id: str
    name: str
    notifications: list[str] = field(default_factory=list)

    def notify(self, message: str) -> None:
        self.notifications.append(message)