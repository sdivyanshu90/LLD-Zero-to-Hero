from __future__ import annotations

import threading
from dataclasses import dataclass, field


@dataclass(slots=True)
class Row:
    row_id: str
    values: dict[str, object]
    lock: threading.Lock = field(default_factory=threading.Lock, repr=False)