# Composition vs. Aggregation

> **The one-line idea:** Composition = *"part-of"* (child dies with parent). Aggregation = *"uses"* (child lives independently).

---

## Composition — Strict Has-A

### Real-World Analogy — House and Rooms

```
┌─────────────────────────────────────────────────────────────┐
│                          HOUSE                              │
│                                                             │
│   ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐       │
│   │  Room   │  │  Room   │  │  Room   │  │  Room   │       │
│   │(Kitchen)│  │(Bedroom)│  │  (Bath) │  │(Living) │       │
│   └─────────┘  └─────────┘  └─────────┘  └─────────┘       │
│                                                             │
│   Rooms ARE PART OF the house.                              │
│   If the house is demolished → the rooms stop existing.    │
│   A room cannot move to another house (it is built-in).    │
└─────────────────────────────────────────────────────────────┘
```

### UML Notation — Filled Diamond (◆)

```
+-------+                +------+
| House | ◆──────────── | Room |
+-------+   1      1..*  +------+
```

- **Filled diamond (◆)** sits on the **owner's** side.
- Read: "House owns one-or-more Rooms."
- Destroying `House` destroys all its `Room` objects.

### More Examples

```
+──────────+                +──────────+
│  Order   │ ◆──────────── │OrderItem │
+──────────+   1     1..*  +──────────+
Delete the order → OrderItems are meaningless.

+──────────────+             +────────────+
│  Document    │ ◆────────── │    Page    │
+──────────────+  1    1..*  +────────────+
A Page only makes sense inside a Document.
```

### The Ownership Test

```
Ask all three questions. If YES to all → Composition.

  1. Can the child exist without this specific parent?   → NO
  2. Does the child's lifecycle match the parent's?      → YES
  3. Is the child physically/logically part of the
     parent's identity?                                  → YES
```

### Code Shape

```
class Order:
    def __init__(self, order_id: str):
        self._order_id = order_id
        self._items: list[OrderItem] = []   # Order creates and owns items

    def add_item(self, product_id: str, quantity: int, price: float) -> None:
        item = OrderItem(product_id, quantity, price)  # ← Order creates child
        self._items.append(item)
```

Key signals: parent **creates** child, child is **not shared**, child is **destroyed with** parent.

---

## Aggregation — Loose Has-A

### Real-World Analogy — Department and Professors

```
┌────────────────────────────────────────────────────────────┐
│                      UNIVERSITY                            │
│                                                            │
│   ┌──────────────┐           ┌─────────────┐              │
│   │  Physics Dept│ ─────────►│  Prof. Kim  │              │
│   └──────────────┘           └─────────────┘              │
│                                     │                      │
│   ┌──────────────┐                  │ (also teaches here)  │
│   │  Math Dept   │ ─────────────────┘                      │
│   └──────────────┘                                         │
│                                                            │
│   Prof. Kim EXISTS independently of any department.        │
│   If Physics Dept is closed → Prof. Kim still exists.      │
│   Prof. Kim can belong to multiple departments.            │
└────────────────────────────────────────────────────────────┘
```

### UML Notation — Open Diamond (◇)

```
+────────────+                  +───────────+
│ Department │ ◇───────────────│ Professor │
+────────────+  0..*      0..* +───────────+
```

- **Open/hollow diamond (◇)** sits on the **container's** side.
- Both multiplicities can be `0..*` — a professor can be in no department.

### More Examples

```
+──────────────+                 +────────────+
│   Playlist   │ ◇────────────── │    Song    │
+──────────────+  0..*     0..*  +────────────+
A Song exists in the library regardless of any playlists.

+──────────────+                 +────────────+
│    Team      │ ◇────────────── │   Player   │
+──────────────+  0..*     0..*  +────────────+
A Player exists beyond a team (free agent, retired, etc.).
```

### The Independence Test

```
Ask all three questions. If YES to all → Aggregation.

  1. Can the child outlive the parent?                        → YES
  2. Can the child be shared between multiple parents?        → YES
  3. Is the child an independently meaningful entity?         → YES
```

### Code Shape

```
class Department:
    def __init__(self, name: str):
        self._name = name
        self._professors: list[Professor] = []   # holds references, doesn't own

    def add_professor(self, professor: Professor) -> None:
        self._professors.append(professor)       # ← receives from outside

    def remove_professor(self, professor: Professor) -> None:
        self._professors.remove(professor)       # ← professor still lives on
```

Key signals: parent **receives** child from outside (injected), child is **not destroyed** with parent, child may be **shared**.

---

## Side-by-Side Comparison

```
┌──────────────────────────┬──────────────────────┬───────────────────────┐
│ DIMENSION                │ COMPOSITION          │ AGGREGATION           │
├──────────────────────────┼──────────────────────┼───────────────────────┤
│ Relationship             │ Strict Has-A         │ Loose Has-A           │
│ Analogy                  │ House + Rooms        │ Dept + Professor      │
│ UML Symbol               │ ◆ (filled diamond)   │ ◇ (open diamond)      │
│ Child created by         │ Parent               │ Outside (injected)    │
│ Child destroyed when     │ Parent destroyed     │ Still lives on        │
│ Child shared?            │ No                   │ Yes (possible)        │
│ Child lifecycle          │ Tied to parent       │ Independent           │
│ Coupling strength        │ Strong               │ Loose                 │
│ Real example             │ Order → OrderItem    │ Team → Player         │
└──────────────────────────┴──────────────────────┴───────────────────────┘
```

### Quick Mnemonic

```
COMPOSITION  =  "Part-of"  =  Filled ◆  =  Born together, die together
AGGREGATION  =  "Uses"     =  Open   ◇  =  Can live apart, possibly shared
```
