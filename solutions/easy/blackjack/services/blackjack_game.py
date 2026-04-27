from dataclasses import dataclass, field

from models.hand import Hand
from services.deck import Deck


@dataclass(slots=True)
class BlackjackGame:
    deck: Deck
    player_hand: Hand = field(default_factory=Hand)
    dealer_hand: Hand = field(default_factory=Hand)

    def deal_initial_cards(self) -> None:
        self.player_hand.add_card(self.deck.deal())
        self.dealer_hand.add_card(self.deck.deal())
        self.player_hand.add_card(self.deck.deal())
        self.dealer_hand.add_card(self.deck.deal())