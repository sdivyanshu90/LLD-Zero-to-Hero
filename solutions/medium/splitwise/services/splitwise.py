from __future__ import annotations

import heapq
from dataclasses import dataclass, field

from models.expense import Expense
from models.member import Member
from models.settlement import Settlement


@dataclass(slots=True)
class SplitwiseService:
    members: dict[str, Member] = field(default_factory=dict)
    balances: dict[str, int] = field(default_factory=dict)

    def add_member(self, member: Member) -> None:
        self.members[member.member_id] = member
        self.balances.setdefault(member.member_id, 0)

    def record_expense(self, expense: Expense) -> None:
        expense.validate()
        self._require_member(expense.paid_by)

        for member_id in expense.shares:
            self._require_member(member_id)

        self.balances[expense.paid_by] += expense.amount_cents
        for member_id, share in expense.shares.items():
            self.balances[member_id] -= share

    def simplify_debts(self) -> list[Settlement]:
        creditors: list[tuple[int, str]] = []
        debtors: list[tuple[int, str]] = []

        for member_id, balance in self.balances.items():
            if balance > 0:
                heapq.heappush(creditors, (-balance, member_id))
            elif balance < 0:
                heapq.heappush(debtors, (balance, member_id))

        settlements: list[Settlement] = []
        while creditors and debtors:
            creditor_balance, creditor_id = heapq.heappop(creditors)
            debtor_balance, debtor_id = heapq.heappop(debtors)

            receivable = -creditor_balance
            payable = -debtor_balance
            settled_amount = min(receivable, payable)
            settlements.append(
                Settlement(
                    from_member_id=debtor_id,
                    to_member_id=creditor_id,
                    amount_cents=settled_amount,
                )
            )

            remaining_credit = receivable - settled_amount
            remaining_debt = payable - settled_amount

            if remaining_credit > 0:
                heapq.heappush(creditors, (-remaining_credit, creditor_id))
            if remaining_debt > 0:
                heapq.heappush(debtors, (-remaining_debt, debtor_id))

        return settlements

    def snapshot_balances(self) -> dict[str, int]:
        return dict(sorted(self.balances.items()))

    def _require_member(self, member_id: str) -> None:
        if member_id not in self.members:
            raise ValueError(f"Unknown member: {member_id}")