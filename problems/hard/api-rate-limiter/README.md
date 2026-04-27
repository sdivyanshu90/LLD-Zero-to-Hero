# API Rate Limiter

## Problem Summary

Design a token-bucket API rate limiter that avoids one global synchronized bottleneck under heavy concurrency.

## Why This Problem Is Asked

Rate limiting appears in every API gateway and every interview about infra-aware backend design. The design test is not just knowing the token-bucket algorithm — it is avoiding a single global lock that serializes all threads. Strong candidates use per-client buckets, each protected by its own lock, so that clients never contend with each other.

Interviewers also probe the TOCTOU race: if `check_tokens()` and `consume_tokens()` are two separate operations, a window exists between them. The correct answer uses an atomic compare-and-decrement inside a single critical section.

## Functional Requirements

1. Rate-limit requests per client key.
2. Refill tokens over time.
3. Allow requests while tokens remain.
4. Reject requests when a bucket is empty.
5. Avoid a single global lock for all clients.

## ASCII UML

```text
+-------------------+
| BucketState       |
+-------------------+
| tokens            |
| last_refill       |
| lock              |
+-------------------+

+-------------------+
| RateLimiter       |
+-------------------+
| stripes           |
| bucket_capacity   |
| refill_rate       |
+-------------------+
| allow()           |
| get_bucket()      |
+-------------------+
```

## Concurrency Checklist

- Shared state: per-client bucket state must be protected.
- Deadlock risk: keep stripe-creation locks separate from bucket-consume locks.
- Lock granularity: use per-bucket or per-stripe locking, not one global lock.
- Lock-free alternative: true CAS-based buckets need lower-level atomic primitives than pure Python exposes.

## SOLID Principles in Play

| Principle | How It Applies                                                                                                                                   |
| --------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| **SRP**   | `TokenBucket` holds tokens and the refill clock for one client. `RateLimiter` manages the bucket registry. Neither leaks into the other.         |
| **OCP**   | Adding a sliding-window algorithm means a new bucket class; `RateLimiter` delegates through the bucket interface unchanged.                      |
| **LSP**   | Any bucket type (token bucket, leaky bucket, fixed window) must satisfy `try_consume() -> bool`; the rate limiter never branches on bucket type. |
| **ISP**   | `TokenBucket` exposes only `try_consume()`. Callers never need to read token counts directly.                                                    |
| **DIP**   | `RateLimiter` holds bucket references through the abstract bucket interface, not a concrete `TokenBucket` class.                                 |

## Key Edge Cases

- Two concurrent requests for the same client must not both succeed when only one token remains.
- A client making its first request must start with a full bucket, not an empty one.
- Refilling a bucket must not overshoot its declared capacity.

## Follow-up Questions

1. How would you implement a sliding-window counter instead of a token bucket?
2. How would you persist bucket state across process restarts?
3. How would you distribute the rate limiter across multiple service instances?
