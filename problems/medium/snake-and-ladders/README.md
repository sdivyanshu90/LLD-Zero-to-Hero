# Snake and Ladders

## Problem Summary

Design a Snake and Ladders game that uses a pluggable dice strategy and validates board initialization so snakes and ladders do not create cycles.

## Why This Problem Is Asked

This problem is a board-game design test with two non-obvious requirements. First, dice behavior should be injectable (Strategy Pattern) so the game is deterministic under test. Second, snakes and ladders must not form a cycle in the jump graph — a board where following jumps loops forever is invalid and should be caught at construction time via DFS cycle detection.

The combination of Strategy for testability and DFS for validation is what separates a strong solution from a naive implementation.

## Functional Requirements

1. Support configurable snakes and ladders.
2. Reject invalid boards with cyclic jumps.
3. Use a dice strategy interface.
4. Advance players turn by turn.
5. Apply snakes and ladders after each move.

## ASCII UML

```text
+-------------------+
| Board             |
+-------------------+
| size              |
| jumps             |
+-------------------+
| validate()        |
| resolve()         |
+-------------------+

+-------------------+
| DiceStrategy      |
+-------------------+
| roll()            |
+-------------------+

+-------------------+
| SnakeLadderGame   |
+-------------------+
| board             |
| players           |
| dice              |
+-------------------+
| take_turn()       |
+-------------------+
```

## SOLID Principles in Play

| Principle | How It Applies                                                                                                                                        |
| --------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| **SRP**   | `Board` validates the jump graph and resolves jumps. `DiceStrategy` encapsulates roll behavior. `SnakeLadderGame` manages turns and player positions. |
| **OCP**   | Adding a `DoubleDice` variant means one new `DiceStrategy` subclass injected at construction; the game loop is unchanged.                             |
| **LSP**   | Any `DiceStrategy` must return a positive integer in the valid range; a strategy returning 0 or a negative number would break `SnakeLadderGame`.      |
| **ISP**   | `DiceStrategy` has one method: `roll() -> int`. Callers never need to inspect how the number is generated.                                            |
| **DIP**   | `SnakeLadderGame` accepts a `DiceStrategy` interface; it never imports `RandomDice` or `FixedDice` directly.                                          |

## Key Edge Cases

- Jumps that form cycles must be rejected.
- A player should not move beyond the last cell.
- Deterministic dice should make the game testable.

## Follow-up Questions

1. How would you add power-up tiles that grant a player a second roll?
2. How would you implement a full replay system using a recorded sequence of dice rolls?
3. How would you adapt the design for a networked multiplayer variant where each player connects remotely?
