from __future__ import annotations

import threading
from dataclasses import dataclass, field

from models.core import Bid, Viewer


@dataclass(slots=True)
class Auction:
    item_id: str
    current_bid: Bid | None = None
    viewers: list[Viewer] = field(default_factory=list)
    _lock: threading.Lock = field(default_factory=threading.Lock, repr=False)

    def subscribe(self, viewer: Viewer) -> None:
        with self._lock:
            self.viewers.append(viewer)

    def place_bid(self, bidder_id: str, amount: int) -> str:
        with self._lock:
            if self.current_bid is not None and amount <= self.current_bid.amount:
                raise ValueError("Bid must be strictly higher than the current bid")
            self.current_bid = Bid(bidder_id=bidder_id, amount=amount)
            viewers = list(self.viewers)

        message = f"{self.item_id}:{bidder_id}:{amount}"
        for viewer in viewers:
            viewer.notify(message)
        return message