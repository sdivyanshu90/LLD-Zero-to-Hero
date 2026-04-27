from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from models.pricing_context import PricingContext
from models.pricing_result import PricingResult
from services.strategies import BulkDiscountStrategy, CouponDiscountStrategy, DiscountStrategy, LoyaltyDiscountStrategy, NoDiscountStrategy


@dataclass(frozen=True, slots=True)
class PricingRule:
    name: str
    priority: int
    strategy: DiscountStrategy
    predicate: Callable[[PricingContext], bool]

    def applies_to(self, context: PricingContext) -> bool:
        return self.predicate(context)


@dataclass(slots=True)
class PricingEngine:
    rules: list[PricingRule]
    fallback_strategy: DiscountStrategy

    def calculate(self, context: PricingContext) -> PricingResult:
        matching_rules = [rule for rule in self.rules if rule.applies_to(context)]
        if not matching_rules:
            final_total = self.fallback_strategy.apply(context.subtotal_cents)
            return PricingResult(
                original_total_cents=context.subtotal_cents,
                final_total_cents=final_total,
                applied_rule="NO_DISCOUNT",
            )

        winning_rule = max(matching_rules, key=lambda rule: rule.priority)
        final_total = winning_rule.strategy.apply(context.subtotal_cents)
        return PricingResult(
            original_total_cents=context.subtotal_cents,
            final_total_cents=final_total,
            applied_rule=winning_rule.name,
        )

    @classmethod
    def default_engine(cls) -> "PricingEngine":
        return cls(
            rules=[
                PricingRule(
                    name="COUPON_20",
                    priority=30,
                    strategy=CouponDiscountStrategy(),
                    predicate=lambda context: context.coupon_code == "SAVE20",
                ),
                PricingRule(
                    name="LOYALTY_10",
                    priority=20,
                    strategy=LoyaltyDiscountStrategy(),
                    predicate=lambda context: context.is_loyal_customer,
                ),
                PricingRule(
                    name="BULK_15",
                    priority=10,
                    strategy=BulkDiscountStrategy(),
                    predicate=lambda context: context.item_count >= 5,
                ),
            ],
            fallback_strategy=NoDiscountStrategy(),
        )