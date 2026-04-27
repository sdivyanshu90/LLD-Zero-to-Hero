from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PricingContext:
    subtotal_cents: int
    item_count: int
    is_loyal_customer: bool
    coupon_code: str | None