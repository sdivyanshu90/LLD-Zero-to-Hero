from dataclasses import dataclass, field

from .card import Card


@dataclass(slots=True)
class Hand:
    cards: list[Card] = field(default_factory=list)

    def add_card(self, card: Card) -> None:
        self.cards.append(card)

    def best_value(self) -> int:
        total = sum(card.base_value() for card in self.cards)
        ace_count = sum(1 for card in self.cards if card.is_ace())

        while ace_count > 0 and total + 10 <= 21:
            total += 10
            ace_count -= 1

        return total

    def is_bust(self) -> bool:
        return self.best_value() > 21