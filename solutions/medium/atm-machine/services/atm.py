from __future__ import annotations

from dataclasses import dataclass

from models.withdrawal_result import WithdrawalResult
from services.handlers import CashHandler


@dataclass(slots=True)
class ATM:
    inventory: dict[int, int]

    def withdraw(self, amount: int) -> dict[int, int]:
        if amount <= 0 or amount % 10 != 0:
            raise ValueError("Withdrawal amount must be positive and divisible by 10")

        draft_inventory = dict(self.inventory)
        chain = self._build_chain(draft_inventory)
        result = chain.dispense(amount, WithdrawalResult())
        if result.remaining_amount != 0:
            raise ValueError(f"Cannot dispense {amount} exactly with current inventory")

        self.inventory = draft_inventory
        return dict(sorted(result.dispensed_notes.items(), reverse=True))

    def snapshot(self) -> dict[int, int]:
        return dict(sorted(self.inventory.items(), reverse=True))

    def _build_chain(self, inventory: dict[int, int]) -> CashHandler:
        ten = CashHandler(10, inventory)
        twenty = CashHandler(20, inventory, next_handler=ten)
        hundred = CashHandler(100, inventory, next_handler=twenty)
        return hundred