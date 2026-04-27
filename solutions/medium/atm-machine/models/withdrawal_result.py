from dataclasses import dataclass, field


@dataclass(slots=True)
class WithdrawalResult:
    dispensed_notes: dict[int, int] = field(default_factory=dict)
    remaining_amount: int = 0