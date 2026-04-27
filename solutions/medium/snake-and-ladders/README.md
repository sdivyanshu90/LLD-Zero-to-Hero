# Snake and Ladders Solution

This implementation validates board jumps, keeps dice behavior pluggable, and applies jumps after each move.

## Design Notes

- `Board` validates special-cell graph cycles.
- `DiceStrategy` makes rolling configurable.
- `SnakeLadderGame` owns turns and player positions.

## Complexity Analysis

| Operation                        | Time                              | Space                                            |
| -------------------------------- | --------------------------------- | ------------------------------------------------ |
| `board.validate()` (cycle check) | O(c), c = number of special cells | O(c) visited set                                 |
| `board.resolve_jump(cell)`       | O(1) dict lookup                  | O(1)                                             |
| `game.take_turn()`               | O(1)                              | O(1)                                             |
| Space (total)                    | —                                 | O(n) for board cells + O(p) for player positions |

## SOLID Compliance

| Principle | Evidence                                                                                                                                |
| --------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| **SRP**   | `Board` owns cell layout and jump resolution. `DiceStrategy` owns roll logic. `SnakeLadderGame` owns turn management and win detection. |
| **OCP**   | A `PowerUpDice` that returns a double roll is one new `DiceStrategy` subclass; the game loop is unchanged.                              |
| **LSP**   | Any `DiceStrategy` must return a positive integer; a strategy returning 0 or negative would break `game.take_turn()`.                   |
| **ISP**   | `DiceStrategy` exposes only `roll() -> int`. Games never need to inspect the internal RNG.                                              |
| **DIP**   | `SnakeLadderGame` accepts a `DiceStrategy` at construction; it never imports `RandomDice` by name in game logic.                        |

## Design Patterns

- **Strategy**: `DiceStrategy.roll()` is swappable; inject a `FixedDice` in tests for deterministic playback.
- **Cycle detection**: `Board.validate()` does a DFS over the jump graph and rejects any configuration where following jumps forms a loop.

## Folder Layout

```text
snake-and-ladders/
|-- app.py
|-- models/
|   |-- board.py
|   `-- player.py
`-- services/
    |-- dice.py
    `-- game.py
```

## Trade-offs

- Board size is fixed at construction; boards are not mutable after creation to keep the cycle-validation guarantee intact.
- `SnakeLadderGame` applies jump resolution iteratively rather than recursively to avoid stack overflow on extreme jump chains.

## Run

From this directory:

```bash
python3 app.py
```
