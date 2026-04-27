from models.pricing_context import PricingContext
from services.pricing_engine import PricingEngine


def main() -> None:
    engine = PricingEngine.default_engine()

    vip_context = PricingContext(subtotal_cents=10_000, item_count=2, is_loyal_customer=True, coupon_code="SAVE20")
    bulk_context = PricingContext(subtotal_cents=8_000, item_count=6, is_loyal_customer=False, coupon_code=None)

    print(engine.calculate(vip_context))
    print(engine.calculate(bulk_context))


if __name__ == "__main__":
    main()