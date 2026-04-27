from models.product import Product
from services.vending_machine import VendingMachine


def main() -> None:
    machine = VendingMachine(
        products=[
            Product(code="A1", name="Soda", price_cents=125, quantity=2),
            Product(code="B2", name="Chips", price_cents=100, quantity=1),
        ]
    )

    print(machine.snapshot())
    print(machine.insert_money(200))
    print(machine.select_product("A1"))
    print(machine.dispense())
    print(machine.snapshot())


if __name__ == "__main__":
    main()