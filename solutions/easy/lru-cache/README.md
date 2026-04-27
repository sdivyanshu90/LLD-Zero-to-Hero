# LRU Cache Solution

This implementation combines a hash map for `O(1)` lookup with a doubly linked list for `O(1)` recency updates.

## Design Notes

- `Node` represents one cache entry in the doubly linked list.
- `LRUCache` owns the linked list and the key-to-node index.
- The head sentinel represents most-recently used side.
- The tail sentinel represents least-recently used side.

## Complexity Analysis

| Operation         | Time         | Space          |
| ----------------- | ------------ | -------------- |
| `get(key)`        | O(1) average | O(1)           |
| `put(key, value)` | O(1) average | O(1) amortized |
| `_evict_lru()`    | O(1)         | O(1)           |
| Space (total)     | —            | O(capacity)    |

Both operations are O(1) because every step is either a dict lookup/delete or a pointer rewire on the doubly linked list — no scanning.

## SOLID Compliance

| Principle | Evidence                                                                                                                                         |
| --------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| **SRP**   | `Node` is pure linked-list state (key, value, prev, next). `LRUCache` owns the algorithm and the index. Neither class leaks into the other.      |
| **OCP**   | Replacing LRU with LFU means rewriting `_evict_lru()` and adding a frequency map — the `get`/`put` interface and `Node` structure are untouched. |
| **LSP**   | `LRUCache` honours the contract that `get()` returns the value or `None`, and `put()` always succeeds within capacity.                           |
| **ISP**   | Callers see only `get()`, `put()`, and `snapshot()`. Private pointer manipulation is invisible.                                                  |
| **DIP**   | `LRUCache` accepts any `Hashable` key; it is not coupled to any concrete key type.                                                               |

## Design Pattern

Hash map + doubly linked list: `dict[key, Node]` delivers O(1) lookup; sentinel-bounded doubly linked list delivers O(1) detach-and-move-to-front on every hit or update.

## Folder Layout

```text
lru-cache/
|-- app.py
|-- models/
|   `-- node.py
`-- services/
    `-- lru_cache.py
```

## Trade-offs

- `_detach` and `_insert_after_head` are private helpers; if you add TTL later, eviction needs to scan by expiry, not just by recency — a separate min-heap for expiry makes that O(log n).
- Thread safety: add a single `RLock` around `get` and `put` for a concurrent version.

## Run

From this directory:

```bash
python app.py
```
