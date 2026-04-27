from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Board:
    size: int
    jumps: dict[int, int]

    def __post_init__(self) -> None:
        self._validate()

    def resolve(self, position: int) -> int:
        return self.jumps.get(position, position)

    def _validate(self) -> None:
        for start, end in self.jumps.items():
            if not 1 < start < self.size or not 1 <= end <= self.size:
                raise ValueError("Jump endpoints must be inside the board")

        visited: set[int] = set()
        path: set[int] = set()

        def dfs(node: int) -> None:
            if node in path:
                raise ValueError("Board jumps contain a cycle")
            if node in visited or node not in self.jumps:
                return
            path.add(node)
            dfs(self.jumps[node])
            path.remove(node)
            visited.add(node)

        for node in self.jumps:
            dfs(node)