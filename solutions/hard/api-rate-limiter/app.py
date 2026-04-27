from services.rate_limiter import StripedTokenBucketLimiter


def main() -> None:
    limiter = StripedTokenBucketLimiter(bucket_capacity=3, refill_rate_per_second=1.0)
    now = 100.0
    print([limiter.allow("client-1", now=now + offset * 0.01) for offset in range(4)])
    print(limiter.allow("client-1", now=104.0))


if __name__ == "__main__":
    main()