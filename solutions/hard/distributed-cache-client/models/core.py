from dataclasses import dataclass, field


@dataclass(slots=True)
class CacheNode:
    node_id: str
    data: dict[str, str] = field(default_factory=dict)