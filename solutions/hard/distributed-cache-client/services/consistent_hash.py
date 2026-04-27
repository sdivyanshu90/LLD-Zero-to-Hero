from __future__ import annotations

import bisect
import hashlib
import threading
from dataclasses import dataclass, field

from models.core import CacheNode


@dataclass(slots=True)
class ConsistentHashRing:
    replicas: int = 3
    nodes: dict[str, CacheNode] = field(default_factory=dict)
    _positions: list[int] = field(default_factory=list, init=False, repr=False)
    _position_to_node: dict[int, str] = field(default_factory=dict, init=False, repr=False)
    _lock: threading.Lock = field(default_factory=threading.Lock, repr=False)

    def add_node(self, node: CacheNode) -> None:
        with self._lock:
            self.nodes[node.node_id] = node
            for replica in range(self.replicas):
                position = self._hash(f"{node.node_id}:{replica}")
                bisect.insort(self._positions, position)
                self._position_to_node[position] = node.node_id

    def remove_node(self, node_id: str) -> None:
        with self._lock:
            node = self.nodes.pop(node_id)
            keys_to_move = list(node.data.items())
            for replica in range(self.replicas):
                position = self._hash(f"{node_id}:{replica}")
                index = bisect.bisect_left(self._positions, position)
                if index < len(self._positions) and self._positions[index] == position:
                    self._positions.pop(index)
                self._position_to_node.pop(position, None)

        for key, value in keys_to_move:
            self.put(key, value)

    def put(self, key: str, value: str) -> None:
        node = self._locate_node(key)
        node.data[key] = value

    def get(self, key: str) -> str | None:
        node = self._locate_node(key)
        return node.data.get(key)

    def snapshot(self) -> dict[str, list[str]]:
        return {node_id: sorted(node.data.keys()) for node_id, node in sorted(self.nodes.items())}

    def _locate_node(self, key: str) -> CacheNode:
        with self._lock:
            if not self._positions:
                raise ValueError("Hash ring is empty")
            position = self._hash(key)
            index = bisect.bisect(self._positions, position) % len(self._positions)
            node_id = self._position_to_node[self._positions[index]]
            return self.nodes[node_id]

    @staticmethod
    def _hash(value: str) -> int:
        return int(hashlib.sha256(value.encode("utf-8")).hexdigest(), 16)