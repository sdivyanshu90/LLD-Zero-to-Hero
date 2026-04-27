# Distributed Cache Client Solution

This implementation uses a consistent-hashing ring with virtual nodes. When a node is removed, only that node's keys are reinserted into the remaining ring.

## Design Notes

- `CacheNode` holds a `node_id` and an in-memory `dict` of key-value pairs.
- `ConsistentHashRing` maintains a sorted list of `(position, node_id)` pairs on the ring, with multiple virtual-node positions per physical node to improve distribution.
- `locate_node()` bisects the sorted positions to find the clockwise successor in O(log n).
- `remove_node()` rehashes all of the removed node's keys into the remaining ring.

## Complexity Analysis

| Operation                                   | Time                                     | Space                                        |
| ------------------------------------------- | ---------------------------------------- | -------------------------------------------- |
| `ring.locate_node(key)`                     | O(log v), v = virtual nodes on ring      | O(1)                                         |
| `ring.add_node(node)`                       | O(r log v) where r = replicas per node   | O(r)                                         |
| `ring.remove_node(node)`                    | O(k + r log v), k = keys on removed node | O(k) rehash                                  |
| `cache_client.get(key)` / `set(key, value)` | O(log v) ring lookup + O(1) dict op      | O(1)                                         |
| Space (total)                               | —                                        | O(n×r) ring positions + O(k) key-value pairs |

## SOLID Compliance

| Principle | Evidence                                                                                                                                          |
| --------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| **SRP**   | `CacheNode` owns local key-value storage. `ConsistentHashRing` owns position management and routing. `CacheClient` coordinates user requests.     |
| **OCP**   | Replication (write to N nodes) means a new `ReplicatedCacheClient` that calls `ring.get_n_nodes(key, n)`; the ring and `CacheNode` are unchanged. |
| **LSP**   | Any `CacheNode` backend (in-memory dict, Redis) satisfies `get(key)` and `set(key, value)`; the ring routes to them uniformly.                    |
| **ISP**   | `ConsistentHashRing` exposes four focused methods; the client never reads raw ring internals.                                                     |
| **DIP**   | `CacheClient` routes to `CacheNode` abstractions; it is not coupled to any concrete storage implementation.                                       |

## Design Pattern

Consistent hashing with virtual nodes: each physical node maps to multiple positions on a fixed-size hash ring (e.g. `hash(f"{node_id}#{i}")`). Adding or removing a node redistributes only the keys that hash between the changed positions, not the entire key space.

## Folder Layout

```text
distributed-cache-client/
|-- app.py
|-- models/
|   `-- core.py            # CacheNode
`-- services/
    `-- consistent_hash.py # ConsistentHashRing
```

## Trade-offs

- Key migration is synchronous on `remove_node()`; in production this would be a background rebalancing job.
- A single ring-level `RLock` serialises all topology changes; per-node locks would allow concurrent reads while a different node is being added.
- Virtual-node count is fixed; a weighted variant adjusts per-node replication factor based on declared capacity.

## Run

From this directory:

```bash
python3 app.py
```
