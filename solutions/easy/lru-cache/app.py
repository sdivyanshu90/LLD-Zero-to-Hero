from services.lru_cache import LRUCache


def main() -> None:
    cache = LRUCache(capacity=2)
    cache.put("A", 1)
    cache.put("B", 2)
    print(cache.snapshot())
    print(cache.get("A"))
    cache.put("C", 3)
    print(cache.snapshot())
    print(cache.get("B"))


if __name__ == "__main__":
    main()