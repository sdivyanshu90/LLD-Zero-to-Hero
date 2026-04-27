# In-Memory Message Broker Solution

This implementation uses per-topic append locks and separate committed-offset synchronization. Consumers only advance committed offsets on `ack`, so uncommitted messages are re-delivered after a crash or restart.

## Design Notes

- `Message` is a frozen dataclass with an `offset` and `payload`.
- `TopicLog` is an append-only list protected by a per-topic `Lock`; `read_from(offset, batch)` is a safe slice.
- `MessageBroker` owns the topic registry and a `committed_offsets` dict protected by a separate lock.
- `poll()` reads from the last committed offset. `ack(consumer, topic, offset)` advances the committed offset only if the new offset is strictly greater.

## Complexity Analysis

| Operation                      | Time                | Space                           |
| ------------------------------ | ------------------- | ------------------------------- |
| `publish(topic, payload)`      | O(1) list append    | O(1)                            |
| `poll(consumer, topic, batch)` | O(batch) slice copy | O(batch)                        |
| `ack(consumer, topic, offset)` | O(1) dict update    | O(1)                            |
| Space (total)                  | —                   | O(total messages across topics) |

Messages are never deleted (log compaction not implemented), so storage grows unboundedly without a retention policy.

## SOLID Compliance

| Principle | Evidence                                                                                                                              |
| --------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| **SRP**   | `TopicLog` owns append and read. `MessageBroker` owns topic registry and offset management. `Message` is a pure data class.           |
| **OCP**   | Adding a compacted topic type means a new `CompactedTopicLog` subclass; `MessageBroker.publish()` routes through the topic interface. |
| **LSP**   | Any topic type must satisfy `append(payload)` and `read_from(offset, batch)`; consumers never branch on topic implementation.         |
| **ISP**   | Producers see only `publish()`. Consumers see only `poll()` and `ack()`. Internal topic locks are invisible.                          |
| **DIP**   | `MessageBroker` holds `TopicLog` references through their abstract interface; it never calls list methods on the log directly.        |

## Design Pattern

Kafka-style at-least-once delivery: the committed offset is the boundary between "delivered and acknowledged" and "pending re-delivery". Separating the append lock (per topic) from the offset lock (broker-wide) allows concurrent publishers on different topics to run in parallel.

## Folder Layout

```text
in-memory-message-broker/
|-- app.py
|-- models/
|   `-- core.py   # Message, TopicLog
`-- services/
    `-- broker.py # MessageBroker
```

## Trade-offs

- Offsets are global across a topic (no partitions). A partitioned model would assign consumers to specific partition ranges.
- The log grows unboundedly; add log compaction or TTL-based pruning to control memory in long-running scenarios.
- `ack()` is non-batching; extend to accept a list of offsets or a high-water mark for throughput-sensitive consumers.

## Run

From this directory:

```bash
python3 app.py
```
