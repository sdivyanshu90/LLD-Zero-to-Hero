from __future__ import annotations

from dataclasses import dataclass, field

from models.product import Product
from models.vend_result import VendResult
from services.states import DispensingState, HasMoneyState, IdleState, VendingState


@dataclass(slots=True)
class VendingMachine:
    products: list[Product]
    balance_cents: int = field(default=0, init=False)
    selected_code: str | None = field(default=None, init=False)
    inventory: dict[str, Product] = field(init=False, repr=False)
    idle_state: IdleState = field(init=False, repr=False)
    has_money_state: HasMoneyState = field(init=False, repr=False)
    dispensing_state: DispensingState = field(init=False, repr=False)
    state: VendingState = field(init=False, repr=False)

    def __post_init__(self) -> None:
        self.inventory = {product.code: product for product in self.products}
        self.idle_state = IdleState()
        self.has_money_state = HasMoneyState()
        self.dispensing_state = DispensingState()
        self.state = self.idle_state

    def set_state(self, state: VendingState) -> None:
        self.state = state

    def insert_money(self, amount_cents: int) -> str:
        return self.state.insert_money(self, amount_cents)

    def select_product(self, code: str) -> str:
        return self.state.select_product(self, code)

    def dispense(self) -> VendResult:
        return self.state.dispense(self)

    def cancel(self) -> int:
        return self.state.cancel(self)

    def get_product(self, code: str) -> Product:
        product = self.inventory.get(code)
        if product is None:
            raise ValueError(f"Unknown product code: {code}")
        return product

    def reset_transaction(self) -> None:
        self.balance_cents = 0
        self.selected_code = None
        self.set_state(self.idle_state)

    def snapshot(self) -> list[str]:
        return [
            f"{product.code} {product.name} price={product.price_cents} quantity={product.quantity}"
            for product in self.inventory.values()
        ]