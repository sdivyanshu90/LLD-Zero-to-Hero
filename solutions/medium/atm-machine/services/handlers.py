from __future__ import annotations

from dataclasses import dataclass

from models.withdrawal_result import WithdrawalResult


@dataclass(slots=True)
class CashHandler:
    denomination: int
    inventory: dict[int, int]
    next_handler: "CashHandler | None" = None

    def dispense(self, amount: int, result: WithdrawalResult) -> WithdrawalResult:
        available = self.inventory.get(self.denomination, 0)
        note_count = min(amount // self.denomination, available)
        if note_count:
            result.dispensed_notes[self.denomination] = note_count
            self.inventory[self.denomination] = available - note_count
            amount -= note_count * self.denomination

        result.remaining_amount = amount
        if amount == 0 or self.next_handler is None:
            return result
        return self.next_handler.dispense(amount, result)