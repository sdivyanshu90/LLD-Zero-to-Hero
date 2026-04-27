from __future__ import annotations

import threading
from dataclasses import dataclass, field


@dataclass(slots=True)
class BucketState:
    tokens: float
    last_refill: float
    lock: threading.Lock = field(default_factory=threading.Lock, repr=False)