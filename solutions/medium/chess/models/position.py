from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Position:
    row: int
    column: int

    @classmethod
    def from_algebraic(cls, notation: str) -> "Position":
        if len(notation) != 2:
            raise ValueError(f"Invalid notation: {notation}")
        column = ord(notation[0].lower()) - ord("a")
        row = int(notation[1]) - 1
        if not 0 <= row < 8 or not 0 <= column < 8:
            raise ValueError(f"Invalid notation: {notation}")
        return cls(row=row, column=column)