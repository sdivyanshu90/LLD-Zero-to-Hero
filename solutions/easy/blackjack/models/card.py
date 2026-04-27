from dataclasses import dataclass
from enum import Enum


class Suit(Enum):
    HEARTS = "hearts"
    DIAMONDS = "diamonds"
    CLUBS = "clubs"
    SPADES = "spades"


class Rank(Enum):
    TWO = "2"
    THREE = "3"
    FOUR = "4"
    FIVE = "5"
    SIX = "6"
    SEVEN = "7"
    EIGHT = "8"
    NINE = "9"
    TEN = "10"
    JACK = "J"
    QUEEN = "Q"
    KING = "K"
    ACE = "A"


@dataclass(frozen=True, slots=True)
class Card:
    suit: Suit
    rank: Rank

    def base_value(self) -> int:
        if self.rank is Rank.ACE:
            return 1
        if self.rank in {Rank.JACK, Rank.QUEEN, Rank.KING}:
            return 10
        return int(self.rank.value)

    def is_ace(self) -> bool:
        return self.rank is Rank.ACE