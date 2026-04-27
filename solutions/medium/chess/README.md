# Chess Solution

This reference implementation focuses on the Command Pattern, undo, redo, and captured-piece restoration. It intentionally keeps move legality simple so the history model stays clear.

## Design Notes

- `ChessBoard` stores pieces by position.
- `MoveCommand` encapsulates execute and undo logic for one move.
- `ChessGame` owns undo and redo stacks.

## Complexity Analysis

| Operation     | Time                      | Space                           |
| ------------- | ------------------------- | ------------------------------- |
| `make_move()` | O(1) — dict insert/lookup | O(1) per command                |
| `undo()`      | O(1) stack pop            | O(1)                            |
| `redo()`      | O(1) stack pop            | O(1)                            |
| Space (total) | —                         | O(m) where m = total moves made |

## SOLID Compliance

| Principle | Evidence                                                                                                                                       |
| --------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| **SRP**   | `MoveCommand` encapsulates one move’s execute and undo. `ChessGame` owns only the undo/redo stacks. `ChessBoard` only manages piece positions. |
| **OCP**   | Adding castling or en passant means a new command subclass; `ChessGame` and `ChessBoard` are unmodified.                                       |
| **LSP**   | All command types satisfy `execute() -> str` and `undo() -> str`; `ChessGame` calls them through the same interface.                           |
| **ISP**   | `MoveCommand` exposes only `execute()` and `undo()`. The captured-piece field is an internal implementation detail.                            |
| **DIP**   | `ChessGame.undo_stack` holds `MoveCommand` references (abstract); it never branches on concrete command types.                                 |

## Design Pattern

Command Pattern: each `MoveCommand` captures the move, the moved piece, and any captured piece at creation time. `execute()` applies the move; `undo()` restores the previous state including captured pieces. A new move after undo clears the redo stack, matching expected command-history semantics.

## Folder Layout

```text
chess/
|-- app.py
|-- models/
|   |-- piece.py
|   |-- position.py
|   `-- move.py
`-- services/
    |-- chess_board.py
    |-- move_command.py
    `-- chess_game.py
```

## Trade-offs

- Legal-move validation is intentionally omitted to keep the command history layer clear and focused.
- Captured piece restoration is unconditional; a real engine would need to handle en passant and promotion separately.

## Run

From this directory:

```bash
python app.py
```
