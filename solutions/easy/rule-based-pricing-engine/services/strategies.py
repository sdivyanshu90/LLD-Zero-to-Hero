from __future__ import annotations

from abc import ABC, abstractmethod


class DiscountStrategy(ABC):
    @abstractmethod
    def apply(self, subtotal_cents: int) -> int:
        raise NotImplementedError


class NoDiscountStrategy(DiscountStrategy):
    def apply(self, subtotal_cents: int) -> int:
        return subtotal_cents


class LoyaltyDiscountStrategy(DiscountStrategy):
    def apply(self, subtotal_cents: int) -> int:
        return max(0, subtotal_cents - int(subtotal_cents * 0.10))


class CouponDiscountStrategy(DiscountStrategy):
    def apply(self, subtotal_cents: int) -> int:
        return max(0, subtotal_cents - int(subtotal_cents * 0.20))


class BulkDiscountStrategy(DiscountStrategy):
    def apply(self, subtotal_cents: int) -> int:
        return max(0, subtotal_cents - int(subtotal_cents * 0.15))