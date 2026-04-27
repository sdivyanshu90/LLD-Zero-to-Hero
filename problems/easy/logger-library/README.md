# Logger Library

## Problem Summary

Design a logger library that exposes one global logger instance and routes messages through a Chain of Responsibility based on log level.

The supported levels are `INFO`, `DEBUG`, and `ERROR`.

## Why This Problem Is Asked

This problem tests two patterns in tandem: Singleton (there is only one logger) and Chain of Responsibility (each handler decides whether to act or pass the message). Seeing both patterns clearly separated is the signal interviewers look for.

A weak answer puts all level-checking inside one `Logger.log()` method. A strong answer shows a chain where each handler is self-contained, unaware of the others' existence, and easily extended with new levels.

## Functional Requirements

1. Expose a singleton logger instance.
2. Accept a log level and message.
3. Route each message to the correct handler through a chain.
4. Preserve logged messages for later inspection.
5. Reject unsupported log levels.

## Constraints

- The singleton rule should be explicit in the design.
- Handlers should be composable; the logger should not be a large `if/elif` switch.
- Keep formatting concerns separated from routing.

## ASCII UML

```text
+-------------------+
| Logger            | <<singleton>>
+-------------------+
| chain_head        |
| _history          |
+-------------------+
| log()             |
| get_history()     |
+-------------------+

+-------------------+
| LogHandler        | <<abstract>>
+-------------------+
| level             |
| next_handler      |
+-------------------+
| handle()          |
+-------------------+
        ^
        |
+-------+-------+
|               |
+---------------+   +---------------+
| InfoHandler   |   | ErrorHandler  |
+---------------+   +---------------+

+-------------------+
| LogRecord         |
+-------------------+
| level             |
| message           |
| timestamp         |
+-------------------+
```

## SOLID Principles in Play

| Principle | How It Applies                                                                                                              |
| --------- | --------------------------------------------------------------------------------------------------------------------------- |
| **SRP**   | `LogRecord` holds event data. `LogHandler` routes and stores. `Logger` provides the global access point.                    |
| **OCP**   | Adding a `WARNING` handler means writing a new class and inserting it in the chain — zero changes to existing handlers.     |
| **LSP**   | Any `LogHandler` subclass can replace another in the chain without breaking routing.                                        |
| **ISP**   | `LogHandler` exposes only `handle()` and `set_next()`. Callers do not know whether the handler stores, prints, or forwards. |
| **DIP**   | `Logger` holds a reference to the `LogHandler` abstract type, not to `InfoHandler` or `ErrorHandler` directly.              |

## Key Edge Cases

- Logging before the chain is initialized must still work.
- Multiple calls to create the logger should return the same instance.
- Unsupported levels should fail fast.

## Suggested Domain Model

- `LogLevel`: supported severity values.
- `LogRecord`: immutable event data.
- `LogHandler`: one link in the responsibility chain.
- `Logger`: singleton entry point.

## Follow-up Questions

1. How would you write to files or remote sinks?
2. How would you support asynchronous logging?
3. How would you add filtering by module or tenant?
