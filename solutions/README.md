# Solutions

This directory contains the runnable Python implementations for each problem.

## Rules

- Every problem solution gets its own folder.
- Every problem folder must contain a `README.md` explaining the design, assumptions, tradeoffs, and how to run the code.
- Do not place the full implementation in a single Python file. Split it across multiple files by responsibility.

## Suggested Problem Layout

```text
solutions/<tier>/<problem-name>/
|-- README.md
|-- app.py
|-- models/
|-- services/
|-- repositories/
`-- utils/
```

The exact folder names can vary by problem, but the code should stay modular and readable.

## Python Guidance

- Use `abc.ABC` for interfaces and contracts.
- Use `dataclass` for simple data containers.
- Use `Enum` for states such as order status or vending machine state.
- Use `threading.Lock` or similar primitives when a problem introduces shared mutable state.
