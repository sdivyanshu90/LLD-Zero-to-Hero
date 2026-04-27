from dataclasses import dataclass, field


@dataclass(slots=True)
class Cell:
    cell_id: str
    value: int = 0
    formula_refs: list[str] = field(default_factory=list)