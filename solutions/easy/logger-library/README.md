# Logger Library Solution

This implementation uses a singleton `Logger` as the public entry point and a Chain of Responsibility to route `INFO`, `DEBUG`, and `ERROR` messages to their matching sinks.

## Design Notes

- `LogRecord` is immutable.
- `LogHandler` models one chain node.
- Each concrete handler decides whether it can process the record or pass it on.
- `Logger` owns the chain and exposes history per level.

## Complexity Analysis

| Operation             | Time                             | Space                        |
| --------------------- | -------------------------------- | ---------------------------- |
| `log(level, message)` | O(k), k ≤ 3 chain links          | O(1)                         |
| `history_for(level)`  | O(h), h = messages at that level | O(h)                         |
| Space (total)         | —                                | O(total log messages stored) |

The chain length is a fixed constant (3 handlers), so `log()` is effectively O(1) at runtime.

## SOLID Compliance

| Principle | Evidence                                                                                                                                  |
| --------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| **SRP**   | `LogRecord` is event data only. `LogHandler` routes and stores. `Logger` is the singleton entry point.                                    |
| **OCP**   | Adding `WARNING` or `CRITICAL` means a new `LogHandler` subclass inserted into the chain — zero changes to existing handlers or `Logger`. |
| **LSP**   | Any `LogHandler` can replace another in the chain; `handle()` is guaranteed to either process or pass on the record.                      |
| **ISP**   | Clients call `log()` and `history_for()`. Chain wiring is an implementation detail of `Logger.__init__()`.                                |
| **DIP**   | `Logger` holds a `LogHandler` reference (abstract type); it never imports `InfoHandler` or `ErrorHandler` by name in its interface.       |

## Design Patterns

- **Singleton**: `Logger.get_instance()` guarantees one global logger.
- **Chain of Responsibility**: `InfoHandler -> DebugHandler -> ErrorHandler`; each handler processes its own level and passes others down the chain.

## Folder Layout

```text
logger-library/
|-- app.py
|-- models/
|   |-- log_level.py
|   `-- log_record.py
`-- services/
    |-- handlers.py
    `-- logger.py
```

## Trade-offs

- History is stored in memory as a list per level; replace with a file sink or rotating buffer for production use.
- Singleton is thread-safe at the class-level initialisation; add a lock inside `get_instance()` if the logger is first created under heavy concurrency.

## Run

From this directory:

```bash
python app.py
```
