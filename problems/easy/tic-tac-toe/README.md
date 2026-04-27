# Tic-Tac-Toe

## Problem Summary

Design an `N x N` Tic-Tac-Toe game that detects wins in `O(1)` time per move.

The key requirement is that win detection must not scan the whole board after every move.

## Why This Problem Is Asked

Win detection is the hidden complexity. Most candidates scan the entire board after each move — O(n²) per move. The insight interviewers want to see is incremental counters: each move updates exactly four values (row sum, column sum, diagonal, anti-diagonal), making win detection O(1).

The N×N generalisation raises a follow-up about the counter design: rather than comparing against a fixed `3`, the target is `N`, and using a +1/−1 weight scheme allows both players to share the same counters.

## Functional Requirements

1. Initialize a board of configurable size.
2. Accept moves from alternating players.
3. Reject invalid or repeated moves.
4. Detect row, column, and diagonal wins in `O(1)` per move.
5. Detect a draw when the board fills without a winner.

## Constraints

- Keep the board model separate from the win-tracking logic.
- Use row, column, and diagonal counters instead of repeated full-board scans.
- The design should support board sizes larger than `3 x 3`.

## ASCII UML

```text
+-------------------+     +-------------------+
| Player            |     | Move              |
+-------------------+     +-------------------+
| player_id         |     | player_id         |
| symbol            |     | row               |
+-------------------+     | col               |
                          +-------------------+

+-------------------+     +-------------------+
| GameBoard         |     | TicTacToeGame     |
+-------------------+     +-------------------+
| size              |     | board             |
| grid              |     | players           |
+-------------------+     | row_counts        |
| place()           |     | col_counts        |
| display()         |     | diag_counts       |
+-------------------+     +-------------------+
                          | make_move()       |
                          | check_winner()    |
                          +-------------------+
```

## SOLID Principles in Play

| Principle | How It Applies                                                                                                                 |
| --------- | ------------------------------------------------------------------------------------------------------------------------------ |
| **SRP**   | `GameBoard` owns grid storage and rendering. `TicTacToeGame` owns the counter logic and turn management.                       |
| **OCP**   | Extending to more than two players requires only a new weight scheme and a different win condition — `GameBoard` is untouched. |
| **LSP**   | `Player` objects are interchangeable; neither `TicTacToeGame` nor `GameBoard` cares about the concrete player type.            |
| **ISP**   | `Move` is a pure data class; game logic does not expose board internals to callers.                                            |
| **DIP**   | `TicTacToeGame` calls `board.place()` through the `GameBoard` interface, not grid array indices directly.                      |

## Key Edge Cases

- Same cell selected twice must fail.
- Moves after the game is over must fail.
- A non-existent player or wrong turn must fail.

## Follow-up Questions

1. How would you support more than two players?
2. How would you persist a game for later resume?
3. What changes if moves come over the network?
