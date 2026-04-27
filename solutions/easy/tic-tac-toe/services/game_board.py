from dataclasses import dataclass, field


@dataclass(slots=True)
class GameBoard:
    size: int
    cells: list[list[str | None]] = field(init=False)

    def __post_init__(self) -> None:
        self.cells = [[None for _ in range(self.size)] for _ in range(self.size)]

    def place(self, row: int, column: int, symbol: str) -> None:
        if not 0 <= row < self.size or not 0 <= column < self.size:
            raise ValueError("Move is outside the board")
        if self.cells[row][column] is not None:
            raise ValueError("Cell is already occupied")
        self.cells[row][column] = symbol

    def render(self) -> list[str]:
        return [" ".join(cell or "." for cell in row) for row in self.cells]