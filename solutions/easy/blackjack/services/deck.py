from dataclasses import dataclass, field

from models.card import Card, Rank, Suit


@dataclass(slots=True)
class Deck:
    cards: list[Card] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.cards:
            self.cards = [Card(suit, rank) for suit in Suit for rank in Rank]

    def deal(self) -> Card:
        if not self.cards:
            raise ValueError("Deck is empty")
        return self.cards.pop(0)