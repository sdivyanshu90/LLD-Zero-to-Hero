from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass, field

from models.core import Cell


@dataclass(slots=True)
class Spreadsheet:
    cells: dict[str, Cell] = field(default_factory=dict)
    dependents: dict[str, set[str]] = field(default_factory=lambda: defaultdict(set))

    def set_value(self, cell_id: str, value: int) -> None:
        cell = self.cells.setdefault(cell_id, Cell(cell_id=cell_id))
        self._clear_dependencies(cell_id, cell.formula_refs)
        cell.formula_refs = []
        cell.value = value
        self._recalculate_all()

    def set_formula(self, cell_id: str, references: list[str]) -> None:
        self.cells.setdefault(cell_id, Cell(cell_id=cell_id))
        self._check_cycle(cell_id, references)
        old_refs = list(self.cells[cell_id].formula_refs)
        self._clear_dependencies(cell_id, old_refs)
        self.cells[cell_id].formula_refs = list(references)
        for reference in references:
            self.cells.setdefault(reference, Cell(cell_id=reference))
            self.dependents[reference].add(cell_id)
        self._recalculate_all()

    def snapshot(self) -> dict[str, int]:
        return {cell_id: cell.value for cell_id, cell in sorted(self.cells.items())}

    def _check_cycle(self, target: str, references: list[str]) -> None:
        graph = {cell_id: list(cell.formula_refs) for cell_id, cell in self.cells.items()}
        graph[target] = list(references)

        visiting: set[str] = set()
        visited: set[str] = set()

        def dfs(node: str) -> None:
            if node in visiting:
                raise ValueError("Spreadsheet formulas contain a cycle")
            if node in visited:
                return
            visiting.add(node)
            for ref in graph.get(node, []):
                dfs(ref)
            visiting.remove(node)
            visited.add(node)

        for node in graph:
            dfs(node)

    def _clear_dependencies(self, cell_id: str, references: list[str]) -> None:
        for reference in references:
            dependents = self.dependents.get(reference)
            if dependents is not None:
                dependents.discard(cell_id)

    def _recalculate_all(self) -> None:
        indegree = {cell_id: len(cell.formula_refs) for cell_id, cell in self.cells.items()}
        queue = deque(cell_id for cell_id, degree in indegree.items() if degree == 0)

        while queue:
            cell_id = queue.popleft()
            cell = self.cells[cell_id]
            if cell.formula_refs:
                cell.value = sum(self.cells[ref].value for ref in cell.formula_refs)
            for dependent in self.dependents.get(cell_id, set()):
                indegree[dependent] -= 1
                if indegree[dependent] == 0:
                    queue.append(dependent)