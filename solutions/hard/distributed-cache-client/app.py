from models.core import CacheNode
from services.consistent_hash import ConsistentHashRing


def main() -> None:
    ring = ConsistentHashRing(replicas=3)
    ring.add_node(CacheNode("N1"))
    ring.add_node(CacheNode("N2"))
    ring.add_node(CacheNode("N3"))

    ring.put("alpha", "A")
    ring.put("beta", "B")
    before = ring.snapshot()
    ring.remove_node("N2")
    after = ring.snapshot()

    print(before)
    print(after)
    print(ring.get("alpha"), ring.get("beta"))


if __name__ == "__main__":
    main()