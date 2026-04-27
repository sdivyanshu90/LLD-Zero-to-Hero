from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field

from models.core import BucketState


@dataclass(slots=True)
class StripedTokenBucketLimiter:
    bucket_capacity: int
    refill_rate_per_second: float
    stripe_count: int = 16
    _stripes: list[dict[str, BucketState]] = field(init=False, repr=False)
    _stripe_locks: list[threading.Lock] = field(init=False, repr=False)

    def __post_init__(self) -> None:
        self._stripes = [dict() for _ in range(self.stripe_count)]
        self._stripe_locks = [threading.Lock() for _ in range(self.stripe_count)]

    def allow(self, client_id: str, now: float | None = None) -> bool:
        current_time = time.monotonic() if now is None else now
        bucket = self._get_bucket(client_id, current_time)
        with bucket.lock:
            elapsed = max(0.0, current_time - bucket.last_refill)
            bucket.tokens = min(self.bucket_capacity, bucket.tokens + elapsed * self.refill_rate_per_second)
            bucket.last_refill = current_time
            if bucket.tokens < 1:
                return False
            bucket.tokens -= 1
            return True

    def _get_bucket(self, client_id: str, now: float) -> BucketState:
        stripe_index = hash(client_id) % self.stripe_count
        stripe = self._stripes[stripe_index]
        lock = self._stripe_locks[stripe_index]
        with lock:
            bucket = stripe.get(client_id)
            if bucket is None:
                bucket = BucketState(tokens=float(self.bucket_capacity), last_refill=now)
                stripe[client_id] = bucket
            return bucket