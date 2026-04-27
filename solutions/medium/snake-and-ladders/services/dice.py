from __future__ import annotations

import random
from abc import ABC, abstractmethod
from dataclasses import dataclass, field


class DiceStrategy(ABC):
    @abstractmethod
    def roll(self) -> int:
        raise NotImplementedError


class StandardDice(DiceStrategy):
    def roll(self) -> int:
        return random.randint(1, 6)


@dataclass(slots=True)
class DeterministicDice(DiceStrategy):
    values: list[int]
    index: int = field(default=0, init=False)

    def roll(self) -> int:
        value = self.values[self.index % len(self.values)]
        self.index += 1
        return value