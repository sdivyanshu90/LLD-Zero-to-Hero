from __future__ import annotations

from dataclasses import dataclass
from typing import Hashable, Optional


@dataclass(slots=True)
class Node:
    key: Optional[Hashable]
    value: object | None
    prev: "Node | None" = None
    next: "Node | None" = None