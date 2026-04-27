from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class Bid:
    bidder_id: str
    amount: int


@dataclass(slots=True)
class Viewer:
    viewer_id: str
    notifications: list[str] = field(default_factory=list)

    def notify(self, message: str) -> None:
        self.notifications.append(message)