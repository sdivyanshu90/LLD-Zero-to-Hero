from dataclasses import dataclass


@dataclass(slots=True)
class Product:
    code: str
    name: str
    price_cents: int
    quantity: int

    def is_available(self) -> bool:
        return self.quantity > 0

    def dispense(self) -> None:
        if not self.is_available():
            raise ValueError(f"Product {self.code} is out of stock")
        self.quantity -= 1