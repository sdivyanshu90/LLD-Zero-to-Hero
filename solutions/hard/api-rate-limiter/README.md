# API Rate Limiter Solution

This reference implementation avoids a single global lock by using striped bucket maps and one lock per client bucket.

True lock-free token-bucket updates require CAS-style atomics that pure Python does not expose in the standard library. This solution therefore uses the smallest practical lock scope instead of claiming false lock-free behavior.

## Design Notes

- `BucketState` holds the current token count, last-refill timestamp, and a per-bucket `Lock`.
- `RateLimiter` keeps a fixed array of stripe maps; a client key is hashed to a stripe to limit stripe-creation contention.
- `allow()` lazily refills tokens based on elapsed time, then consumes one token if available.

## Complexity Analysis

| Operation          | Time                                         | Space                                |
| ------------------ | -------------------------------------------- | ------------------------------------ |
| `allow(client_id)` | O(1) — hash to stripe, lock, refill, consume | O(1)                                 |
| Stripe lookup      | O(1) via modular hash                        | O(1)                                 |
| Space (total)      | —                                            | O(c) where c = unique active clients |

Lock contention is bounded per stripe: `n` stripes means at most `c/n` clients compete per lock on average.

## SOLID Compliance

| Principle | Evidence                                                                                                                                                                              |
| --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **SRP**   | `BucketState` owns token tracking and the refill clock. `RateLimiter` owns stripe management and the `allow()` entry point.                                                           |
| **OCP**   | Replacing the token-bucket algorithm with a leaky-bucket or sliding-window means a new `BucketState` implementation injected into the stripe map; the `RateLimiter` API is unchanged. |
| **LSP**   | Any `BucketState` implementation must satisfy `try_consume() -> bool` without side effects outside the bucket.                                                                        |
| **ISP**   | Callers call only `allow(client_id) -> bool`; they never read bucket internals.                                                                                                       |
| **DIP**   | `RateLimiter` references buckets through their `try_consume()` interface; it is not coupled to `TokenBucketState` by name in `allow()`.                                               |

## Design Pattern

Striped locking (lock striping): instead of one global dict lock, the key space is divided into N stripes, each with its own `Lock`. Clients in different stripes never block each other. This is the same pattern used in `java.util.concurrent.ConcurrentHashMap`.

## Folder Layout

```text
api-rate-limiter/
|-- app.py
|-- models/
|   `-- core.py        # BucketState
`-- services/
    `-- rate_limiter.py # RateLimiter
```

## Trade-offs

- Refill is lazy (computed on `allow()` calls); a background refill thread would be needed for pre-warming buckets.
- Stripe count is fixed at construction; hot-spot detection would require dynamic resizing not available in this version.
- Time source is `time.monotonic()`; safe from clock adjustments, unlike `time.time()`.

## Run

From this directory:

```bash
python3 app.py
```
