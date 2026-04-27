from __future__ import annotations

from dataclasses import dataclass, field
from typing import Hashable

from models.node import Node


@dataclass(slots=True)
class LRUCache:
    capacity: int
    _items: dict[Hashable, Node] = field(default_factory=dict, init=False, repr=False)
    _head: Node = field(init=False, repr=False)
    _tail: Node = field(init=False, repr=False)

    def __post_init__(self) -> None:
        if self.capacity <= 0:
            raise ValueError("Capacity must be positive")

        self._head = Node(None, None)
        self._tail = Node(None, None)
        self._head.next = self._tail
        self._tail.prev = self._head

    def get(self, key: Hashable) -> object | None:
        node = self._items.get(key)
        if node is None:
            return None

        self._move_to_front(node)
        return node.value

    def put(self, key: Hashable, value: object) -> None:
        node = self._items.get(key)
        if node is not None:
            node.value = value
            self._move_to_front(node)
            return

        node = Node(key, value)
        self._items[key] = node
        self._add_after_head(node)

        if len(self._items) > self.capacity:
            self._evict_lru()

    def snapshot(self) -> list[tuple[Hashable, object | None]]:
        current = self._head.next
        entries: list[tuple[Hashable, object | None]] = []
        while current is not None and current is not self._tail:
            entries.append((current.key, current.value))
            current = current.next
        return entries

    def _move_to_front(self, node: Node) -> None:
        self._detach(node)
        self._add_after_head(node)

    def _add_after_head(self, node: Node) -> None:
        first = self._head.next
        node.prev = self._head
        node.next = first
        self._head.next = node
        if first is not None:
            first.prev = node

    def _detach(self, node: Node) -> None:
        previous = node.prev
        following = node.next
        if previous is not None:
            previous.next = following
        if following is not None:
            following.prev = previous

    def _evict_lru(self) -> None:
        node = self._tail.prev
        if node is None or node is self._head or node.key is None:
            raise RuntimeError("Cannot evict from an empty cache")

        self._detach(node)
        del self._items[node.key]