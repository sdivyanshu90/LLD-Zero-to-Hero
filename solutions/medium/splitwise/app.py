from models.expense import Expense
from models.member import Member
from services.splitwise import SplitwiseService


def main() -> None:
    service = SplitwiseService()
    service.add_member(Member(member_id="A", name="Asha"))
    service.add_member(Member(member_id="B", name="Bharat"))
    service.add_member(Member(member_id="C", name="Charu"))

    service.record_expense(
        Expense(
            description="Dinner",
            paid_by="A",
            amount_cents=6000,
            shares={"A": 2000, "B": 2000, "C": 2000},
        )
    )
    service.record_expense(
        Expense(
            description="Cab",
            paid_by="B",
            amount_cents=3000,
            shares={"A": 1000, "B": 1000, "C": 1000},
        )
    )

    print(service.snapshot_balances())
    print(service.simplify_debts())


if __name__ == "__main__":
    main()