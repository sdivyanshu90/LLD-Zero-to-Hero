from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Settlement:
    from_member_id: str
    to_member_id: str
    amount_cents: int