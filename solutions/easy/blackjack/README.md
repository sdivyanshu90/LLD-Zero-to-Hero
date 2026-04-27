# Blackjack Solution

This implementation keeps dynamic Ace scoring inside `Hand` so totals adjust automatically as cards are added.

## Design Notes

- `Card` models rank and suit.
- `Hand` computes the best non-busting score in real time.
- `Deck` owns dealing order.
- `BlackjackGame` coordinates the player and dealer hands.

## Complexity Analysis

| Operation           | Time                             | Space                          |
| ------------------- | -------------------------------- | ------------------------------ |
| `hand.best_value()` | O(a), a = number of Aces in hand | O(1)                           |
| `hand.add_card()`   | O(1)                             | O(1)                           |
| `deck.deal_card()`  | O(1) (list pop from end)         | O(1)                           |
| Space (total)       | —                                | O(52) for deck + O(h) per hand |

`best_value()` counts Aces separately and greedily promotes each from 1 to 11, so its runtime is proportional to the number of Aces, not the total hand size.

## SOLID Compliance

| Principle | Evidence                                                                                                                                             |
| --------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| **SRP**   | `Card` = identity. `Hand` = scoring. `Deck` = dealing. `BlackjackGame` = round orchestration. Each class has exactly one reason to change.           |
| **OCP**   | Changing Ace value rules (e.g., always count as 1) is isolated to `Hand.best_value()` with no impact on `Card`, `Deck`, or `BlackjackGame`.          |
| **LSP**   | Any `Card` added to a `Hand` must return a valid `hard_value()` integer — no `None` returns that would break `best_value()`.                         |
| **ISP**   | `Hand` only exposes `add_card()`, `best_value()`, and `is_bust()`. Deck internals are hidden.                                                        |
| **DIP**   | `BlackjackGame` depends on `Hand` and `Deck` through their public interfaces; injecting a `FixedDeck` for tests requires zero changes to game logic. |

## Design Pattern

Strategy-like Ace scoring: `Hand.best_value()` iterates Aces last, upgrading each from 1 to 11 as long as the total stays under 21. No special cases per combination.

## Folder Layout

```text
blackjack/
|-- app.py
|-- models/
|   |-- card.py
|   `-- hand.py
`-- services/
    |-- deck.py
    `-- blackjack_game.py
```

## Trade-offs

- `Deck` is a simple list shuffle. Swap to a seeded shuffle for deterministic tests.
- Dealer AI is a hit-below-17 rule; move it to a separate strategy to vary difficulty.

## Run

From this directory:

```bash
python app.py
```
