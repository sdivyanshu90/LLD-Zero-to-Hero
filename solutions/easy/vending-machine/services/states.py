from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from models.vend_result import VendResult

if TYPE_CHECKING:
    from services.vending_machine import VendingMachine


class VendingState(ABC):
    @abstractmethod
    def insert_money(self, machine: "VendingMachine", amount_cents: int) -> str:
        raise NotImplementedError

    @abstractmethod
    def select_product(self, machine: "VendingMachine", code: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def dispense(self, machine: "VendingMachine") -> VendResult:
        raise NotImplementedError

    @abstractmethod
    def cancel(self, machine: "VendingMachine") -> int:
        raise NotImplementedError


class IdleState(VendingState):
    def insert_money(self, machine: "VendingMachine", amount_cents: int) -> str:
        if amount_cents <= 0:
            raise ValueError("Inserted money must be positive")
        machine.balance_cents += amount_cents
        machine.set_state(machine.has_money_state)
        return f"Balance is now {machine.balance_cents} cents"

    def select_product(self, machine: "VendingMachine", code: str) -> str:
        raise ValueError("Insert money before selecting a product")

    def dispense(self, machine: "VendingMachine") -> VendResult:
        raise ValueError("Select a product before dispensing")

    def cancel(self, machine: "VendingMachine") -> int:
        return 0


class HasMoneyState(VendingState):
    def insert_money(self, machine: "VendingMachine", amount_cents: int) -> str:
        if amount_cents <= 0:
            raise ValueError("Inserted money must be positive")
        machine.balance_cents += amount_cents
        return f"Balance is now {machine.balance_cents} cents"

    def select_product(self, machine: "VendingMachine", code: str) -> str:
        product = machine.get_product(code)
        if not product.is_available():
            raise ValueError(f"Product {code} is out of stock")
        if machine.balance_cents < product.price_cents:
            raise ValueError("Insufficient balance for selected product")

        machine.selected_code = code
        machine.set_state(machine.dispensing_state)
        return f"Selected {product.name}"

    def dispense(self, machine: "VendingMachine") -> VendResult:
        raise ValueError("Select a product before dispensing")

    def cancel(self, machine: "VendingMachine") -> int:
        refund = machine.balance_cents
        machine.reset_transaction()
        return refund


class DispensingState(VendingState):
    def insert_money(self, machine: "VendingMachine", amount_cents: int) -> str:
        raise ValueError("Cannot insert money while dispensing")

    def select_product(self, machine: "VendingMachine", code: str) -> str:
        raise ValueError("Already selected a product")

    def dispense(self, machine: "VendingMachine") -> VendResult:
        if machine.selected_code is None:
            raise RuntimeError("No product selected")

        product = machine.get_product(machine.selected_code)
        product.dispense()
        change = machine.balance_cents - product.price_cents
        result = VendResult(product_code=product.code, product_name=product.name, change_cents=change)
        machine.reset_transaction()
        return result

    def cancel(self, machine: "VendingMachine") -> int:
        raise ValueError("Cannot cancel while dispensing")