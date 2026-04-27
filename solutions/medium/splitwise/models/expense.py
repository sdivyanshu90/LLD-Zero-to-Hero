from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Expense:
    description: str
    paid_by: str
    amount_cents: int
    shares: dict[str, int]

    def validate(self) -> None:
        if self.amount_cents <= 0:
            raise ValueError("Expense amount must be positive")
        if sum(self.shares.values()) != self.amount_cents:
            raise ValueError("Shares must sum exactly to the expense amount")