from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class VendResult:
    product_code: str
    product_name: str
    change_cents: int