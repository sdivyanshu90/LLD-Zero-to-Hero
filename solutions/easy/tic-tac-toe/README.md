# Tic-Tac-Toe Solution

This implementation separates board state from `O(1)` win detection using signed row, column, and diagonal counters.

## Design Notes

- `Player` defines identity and symbol.
- `Move` captures one turn.
- `GameBoard` owns cell occupancy.
- `TicTacToeGame` owns turn order, counters, and winner detection.

## Complexity Analysis

| Operation     | Time                                           | Space                                      |
| ------------- | ---------------------------------------------- | ------------------------------------------ |
| `play_move()` | O(1) — four counter updates + four comparisons | O(1)                                       |
| `render()`    | O(n²)                                          | O(n²) output                               |
| Space (total) | —                                              | O(n²) for grid + O(n) for row/col counters |

Win detection is O(1) because `play_move()` only checks the four totals that the current move could have changed.

## SOLID Compliance

| Principle | Evidence                                                                                                                            |
| --------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| **SRP**   | `GameBoard` stores and renders the grid. `TicTacToeGame` tracks counters, turns, and winner state. Two separate reasons to change.  |
| **OCP**   | Extending to a 5-in-a-row game (Gomoku) means adjusting the win target and board size in `TicTacToeGame`; `GameBoard` is untouched. |
| **LSP**   | `Player` objects are substitutable; the game never inspects a player's concrete type.                                               |
| **ISP**   | `GameBoard` only exposes `place()` and `render()`; `TicTacToeGame` never touches the raw grid array.                                |
| **DIP**   | `TicTacToeGame` calls `self.board.place()` through the `GameBoard` interface, never through direct array access.                    |

## Design Pattern

O(1) win detection via signed counters: each player has its own sign (+1 or -1). A row, column, or diagonal counter reaching `±N` means that player filled the line — no board scan needed.

## Folder Layout

```text
tic-tac-toe/
|-- app.py
|-- models/
|   |-- player.py
|   `-- move.py
`-- services/
    |-- game_board.py
    `-- tic_tac_toe.py
```

## Trade-offs

- Works for any N×N board and any number of players as long as each player gets a unique sign. For more than two players, use a dictionary of `{player_id: counter_array}` instead of a single signed int.
- `GameBoard` stores the grid for display only; win detection never reads from it, which is intentional.

## Run

From this directory:

```bash
python app.py
```
