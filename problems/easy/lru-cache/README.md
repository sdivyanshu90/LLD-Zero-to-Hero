# LRU Cache

## Problem Summary

Design an in-memory Least Recently Used cache with `O(1)` average-time `get()` and `put()` operations.

When the cache reaches capacity, it must evict the least recently used item before inserting a new one.

## Why This Problem Is Asked

This is the most common data structure design question in software engineering interviews. The interview test is whether the candidate knows the _why_: a doubly linked list gives O(1) detach-and-reinsert; a plain list or `collections.OrderedDict` shortcut skips the learning entirely.

A strong answer shows that the candidate can compose a hashmap with a linked list, name each component's responsibility, and identify the sentinel-node trick that eliminates edge-case checks for empty lists.

## Functional Requirements

1. Return the cached value for a key if it exists.
2. Mark a key as most recently used whenever it is read or updated.
3. Insert a new key-value pair.
4. Evict exactly one least recently used entry when capacity is full.
5. Expose the cache order for debugging.

## Constraints

- Both `get()` and `put()` should run in `O(1)` average time.
- Do not fake `O(1)` behavior by scanning a list or sorting on every call.
- Keep the cache logic separated from the node structure.

## ASCII UML

```text
+-------------------+     +-------------------+
| Node              |     | LRUCache          |
+-------------------+     +-------------------+
| key               |     | capacity          |
| value             |     | index             |
| prev              |<--->| head (MRU)        |
| next              |     | tail (LRU)        |
+-------------------+     +-------------------+
                          | get()             |
                          | put()             |
                          | order()           |
                          +-------------------+
```

## SOLID Principles in Play

| Principle | How It Applies                                                                                                                                 |
| --------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| **SRP**   | `Node` is pure linked-list state (key, value, pointers). `LRUCache` owns the algorithm and the index. Neither bleeds into the other.           |
| **OCP**   | The eviction policy (LRU) is isolated in `_evict_lru()`. Replacing it with LFU means rewriting that one method, not rewriting the whole class. |
| **LSP**   | Not directly applicable here, but `LRUCache` should satisfy any contract of a generic `Cache` abstract base if one exists.                     |
| **ISP**   | Callers only see `get()` and `put()`; internal list manipulation methods are private.                                                          |
| **DIP**   | `LRUCache` does not depend on a concrete key type — it accepts any `Hashable`.                                                                 |

## Key Edge Cases

- Updating an existing key must not increase the cache size.
- Reading a missing key should return a clear miss signal.
- Capacity must be positive.
- Repeated reads of the same key should keep that key at the front of the recency order.

## Suggested Domain Model

- `Node`: one entry in a doubly linked list.
- `LRUCache`: owns the hash map and linked-list orchestration.

The design test here is whether the candidate knows why the doubly linked list exists: constant-time detach and reinsert.

## Follow-up Questions

1. How would you make this cache thread-safe?
2. How would you add time-based expiry?
3. How would you support weighted eviction instead of count-based eviction?
