from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PricingResult:
    original_total_cents: int
    final_total_cents: int
    applied_rule: str