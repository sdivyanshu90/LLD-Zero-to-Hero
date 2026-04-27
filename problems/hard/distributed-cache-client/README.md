# Distributed Cache Client

## Problem Summary

Design a distributed cache client that uses a consistent-hashing ring so node failure redistributes only the failed node's keys.

## Why This Problem Is Asked

Consistent hashing is a fundamental algorithm used in Redis Cluster, DynamoDB, and Cassandra. The interview test is knowing _why_ it exists: naive modular hashing `hash(key) % n` remaps nearly all keys when n changes; consistent hashing bounds the remapping to the departed node’s keys only.

Virtual nodes are the follow-up: a single physical node maps to many ring positions, making load distribution uniform even with heterogeneous node capacities. Candidates who know virtual nodes signal senior-level distributed systems awareness.

## Functional Requirements

1. Add and remove cache nodes dynamically.
2. Hash node positions onto a ring to minimise key redistribution on topology changes.
3. Locate the responsible node for any given key using clockwise ring traversal.
4. Put and get key-value pairs on the correct node.
5. Redistribute a removed node's keys to its ring successor.

## ASCII UML

```text
+-------------------+
| CacheNode         |
+-------------------+
| node_id           |
| data              |
+-------------------+

+-------------------+
| ConsistentHashRing|
+-------------------+
| positions         |
| nodes             |
+-------------------+
| add_node()        |
| remove_node()     |
| locate_node()     |
| put()             |
| get()             |
+-------------------+
```

## Concurrency Checklist

- Shared state: ring membership and node-local maps.
- Deadlock risk: keep membership changes and key movement simple and ordered.
- Lock granularity: one ring lock plus per-node maps is enough for this reference version.
- Lock-free alternative: immutable ring snapshots with atomic swaps.

## SOLID Principles in Play

| Principle | How It Applies                                                                                                                                                |
| --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **SRP**   | `ConsistentHashRing` owns the ring, node mapping, and key routing. `CacheNode` represents one node’s storage. `CacheClient` coordinates get/set across nodes. |
| **OCP**   | Adding replication means a new `ReplicatedCacheClient` that uses the ring to find N replicas; the ring itself is unchanged.                                   |
| **LSP**   | Any `CacheNode` implementation (in-memory, Redis, Memcached) satisfies `get(key)` and `set(key, value)`; the client uses them uniformly.                      |
| **ISP**   | `ConsistentHashRing` exposes only `get_node(key)`, `add_node()`, and `remove_node()`. Callers never need to read ring internals.                              |
| **DIP**   | `CacheClient` routes through the ring to a `CacheNode` abstraction; it is not coupled to any specific storage backend.                                        |

## Key Edge Cases

- Removing a node must migrate its keys to the ring successor, not lose them.
- Adding a new node may claim some keys from its successor; those keys must move correctly.
- Locating a key on an empty ring must fail with a clear error.

## Follow-up Questions

1. How would you add replication so each key lives on two nodes for fault tolerance?
2. How would you implement read-your-writes consistency after a node is added?
3. How would you handle network partitions between the client and one cache node?
