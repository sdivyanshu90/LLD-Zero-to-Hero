from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Member:
    member_id: str
    name: str