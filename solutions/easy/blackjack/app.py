from models.card import Card, Rank, Suit
from services.blackjack_game import BlackjackGame
from services.deck import Deck


def main() -> None:
    scripted_cards = [
        Card(Suit.SPADES, Rank.ACE),
        Card(Suit.HEARTS, Rank.SEVEN),
        Card(Suit.CLUBS, Rank.NINE),
        Card(Suit.DIAMONDS, Rank.KING),
    ]
    game = BlackjackGame(deck=Deck(cards=scripted_cards))
    game.deal_initial_cards()

    print(game.player_hand.best_value())
    print(game.dealer_hand.best_value())
    print(game.player_hand.is_bust())


if __name__ == "__main__":
    main()