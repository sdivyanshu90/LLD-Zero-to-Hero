# Blackjack

## Problem Summary

Design a small Blackjack model that computes hand values dynamically, especially for Aces, which can count as `1` or `11` depending on the current hand.

The score calculation must be correct in real time without hardcoded special cases for specific card combinations.

## Why This Problem Is Asked

The Ace scoring problem is a classic modeling challenge: two Aces in hand must be counted as 1+1 or 11+1, not 11+11. A strong design iterates the hand once, counts hard totals, then greedily promotes each Ace from 1 to 11 as long as the total stays ≤ 21. This avoids any explicit case matching on combination size.

Interviewers use this to verify that a candidate models rules as algorithms rather than lookup tables, and keeps scoring logic inside the `Hand` class rather than in the game orchestrator.

## Functional Requirements

1. Model cards, suits, and ranks.
2. Represent a hand that can accept new cards.
3. Compute the best valid hand value dynamically.
4. Detect busts.
5. Support basic dealing from a deck.

## Constraints

- Ace handling must be generic, not a pile of explicit `if` branches for each case.
- Keep deck behavior separate from hand scoring.
- Face cards should count as `10`.

## ASCII UML

```text
+-------------------+     +-------------------+
| Card              |     | Hand              |
+-------------------+     +-------------------+
| rank              |<>-->| cards             |
| suit              |     +-------------------+
+-------------------+     | add_card()        |
                          | best_value()      |
                          | is_bust()         |
                          +-------------------+

+-------------------+     +-------------------+
| Deck              |     | BlackjackGame     |
+-------------------+     +-------------------+
| cards             |     | player_hand       |
+-------------------+     | dealer_hand       |
| deal_card()       |     | deck              |
+-------------------+     +-------------------+
                          | deal()            |
                          | play_round()      |
                          +-------------------+
```

## SOLID Principles in Play

| Principle | How It Applies                                                                                                                                  |
| --------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| **SRP**   | `Card` is rank + suit only. `Hand` owns scoring. `Deck` owns dealing. `BlackjackGame` orchestrates rounds. Each class has one reason to change. |
| **OCP**   | A new variant (e.g., Spanish 21, where tens are removed) only changes `Card.hard_value()` and the deck contents — game logic is unaffected.     |
| **LSP**   | Any `Card` subtype (e.g., a joker) must still produce a valid `hard_value()` without breaking `Hand.best_value()`.                              |
| **ISP**   | `Hand` only needs `add_card()` and `best_value()`. Dealing mechanics stay inside `Deck`.                                                        |
| **DIP**   | `BlackjackGame` depends on `Hand` and `Deck` abstractions; a test double can replace `Deck` with a fixed sequence.                              |

## Key Edge Cases

- Multiple Aces in the same hand.
- Busting after initially soft totals.
- Empty hand values.

## Follow-up Questions

1. How would you add split and double-down?
2. How would you model dealer rules like hit-on-soft-17?
3. How would you make dealing deterministic for tests?
