# Chess

## Problem Summary

Design the move history layer for a chess game using the Command Pattern.

Each move must be executable, undoable, and redoable, including full restoration of any captured piece.

## Why This Problem Is Asked

Chess move history is the textbook Command Pattern application. The depth test is captured-piece restoration on undo: a candidate who stores only the source and destination square cannot undo correctly when a piece is taken. The command must snapshot the captured piece at creation time.

Interviewers also probe the redo-clearing rule: making a new move after an undo must erase the redo stack, which is the expected behavior in any editor or game with undo history.

## Functional Requirements

1. Represent pieces and positions.
2. Move a piece from one square to another.
3. Capture pieces.
4. Undo a move and fully restore board state.
5. Redo an undone move.

## Constraints

- Use a command object per move.
- Undo and redo should operate on move history, not ad hoc snapshots in the UI.
- Keep board storage separate from move-history orchestration.

## ASCII UML

```text
+-------------------+
| Position          |
+-------------------+
| row               |
| column            |
+-------------------+

+-------------------+
| Piece             |
+-------------------+
| piece_type        |
| color             |
+-------------------+

+-------------------+
| ChessMove         |
+-------------------+
| from_position     |
| to_position       |
+-------------------+

+-------------------+       +-------------------+
| MoveCommand       |------>| ChessBoard        |
+-------------------+       +-------------------+
| move              |       | pieces_by_position|
| moved_piece       |       +-------------------+
| captured_piece    |       | place_piece()     |
+-------------------+       | apply_move()      |
| execute()         |       | restore_piece()   |
| undo()            |       +-------------------+
+-------------------+

+-------------------+
| ChessGame         |
+-------------------+
| undo_stack        |
| redo_stack        |
+-------------------+
| make_move()       |
| undo()            |
| redo()            |
+-------------------+
```

## SOLID Principles in Play

| Principle | How It Applies                                                                                                                                          |
| --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **SRP**   | `MoveCommand` encapsulates one move’s execute and undo logic. `ChessGame` manages only the undo/redo stacks. `ChessBoard` manages only piece positions. |
| **OCP**   | Adding a castling command means a new `CastlingCommand` class; `ChessGame` and `ChessBoard` are untouched.                                              |
| **LSP**   | All command types satisfy `execute() -> str` and `undo() -> str`; `ChessGame` can call them uniformly.                                                  |
| **ISP**   | `MoveCommand` exposes only `execute()` and `undo()`; game history tracking never needs to inspect the move internals.                                   |
| **DIP**   | `ChessGame` holds a list of `MoveCommand` abstract references; it never calls concrete move logic directly.                                             |

## Key Edge Cases

- Undo after a capture must restore both pieces correctly.
- A new move after undo should clear redo history.
- Moving from an empty square should fail.

## Follow-up Questions

1. How would you add legal-move validation per piece type?
2. How would you detect check and checkmate?
3. How would you serialize and replay a full game?
