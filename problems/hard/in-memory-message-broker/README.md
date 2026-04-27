# In-Memory Message Broker

## Problem Summary

Design a Kafka-like in-memory message broker with concurrent producers, consumer offset tracking, and crash recovery without duplicating committed work.

## Why This Problem Is Asked

Message brokers are core infrastructure in event-driven architectures. This problem tests whether a candidate understands offset-based consumption (as opposed to destructive dequeue), which is what enables replay, at-least-once delivery, and crash recovery without data loss.

The two hardest parts are lock granularity (producers write different topics; they should not block each other) and offset atomicity (a consumer must not advance its offset before the message is fully processed, or a crash between processing and offset-commit duplicates work).

## Functional Requirements

1. Support topics with append-only logs.
2. Allow concurrent publishers.
3. Poll messages from a committed consumer offset.
4. Commit offsets only after acknowledgment.
5. Re-deliver uncommitted messages after consumer restart.

## ASCII UML

```text
+-------------------+
| Message           |
+-------------------+
| offset            |
| payload           |
+-------------------+

+-------------------+
| TopicLog          |
+-------------------+
| messages          |
| lock              |
+-------------------+
| append()          |
| read_from()       |
+-------------------+

+-------------------+
| MessageBroker     |
+-------------------+
| topics            |
| committed_offsets |
+-------------------+
| publish()         |
| poll()            |
| ack()             |
+-------------------+
```

## Concurrency Checklist

- Shared state: topic logs and committed offsets must be synchronized.
- Deadlock risk: keep topic-log locks and offset locks disjoint and short-lived.
- Lock granularity: per-topic locks are better than one broker-wide log lock.
- Lock-free alternative: a real append log would typically rely on lower-level atomics or durable storage primitives.

## SOLID Principles in Play

| Principle | How It Applies                                                                                                                   |
| --------- | -------------------------------------------------------------------------------------------------------------------------------- |
| **SRP**   | `Topic` owns its append-only log. `Consumer` owns its offset. `MessageBroker` coordinates topic creation and routing.            |
| **OCP**   | Adding a compacted topic variant means a new `CompactedTopic` subclass; the broker’s publish/subscribe interface is unchanged.   |
| **LSP**   | Any topic type must satisfy `append(message)` and `read_from(offset)`; consumers never branch on topic type.                     |
| **ISP**   | `Consumer` only needs `poll()` and `commit_offset()`; it does not need to know how the topic log is stored.                      |
| **DIP**   | `MessageBroker` holds `Topic` references through their abstract interface; it never imports log implementation classes directly. |

## Key Edge Cases

- Polling past the end of a topic log must return an empty list, not an error.
- A consumer that crashes before acknowledging must re-receive the same messages on next poll.
- Publishing to a nonexistent topic must fail fast with a clear error.

## Follow-up Questions

1. How would you add consumer groups where multiple consumers share a topic with partition-level offsets?
2. How would you implement message TTL and automatic log compaction to reclaim memory?
3. How would you persist the append log to disk so messages survive process restarts?
