"""Order checkout.

The rules live in `src/shop/specs/checkout.md` - read it first.
Both functions below are stubs: their signature is final, the bodies are yours.
Do not change the constants: the tests rely on them.
"""

import re
import sys

PROMO_CODES = {"WELCOME10": 10, "SUMMER15": 15, "VIP35": 35}
SUPPORTED_CITIES = ("msk", "spb")
MAX_DISCOUNT_PERCENT = 30
VAT_PERCENT = 20
SHIPPING_KOPEKS = 49_000
FREE_DELIVERY_FROM_KOPEKS = 500_000
TIER_DISCOUNTS = ((10, 5), (25, 10), (50, 15))
REQUIRED_LINE_KEYS = ("sku", "qty", "unit_price_kopecks")


def _parse_integer(value: str) -> int | None:
    """Parse decimal export values without exceptions, including signs and underscores."""
    text = value.strip()
    if re.fullmatch(r"[+-]?\d(?:_?\d)*", text) is None:
        return None
    limit = sys.get_int_max_str_digits()
    if limit and sum(character.isdecimal() for character in text) > limit:
        return None
    return int(text)


def _validate_line(line: dict[str, str], number: int) -> str | None:
    """Validate the fields before any arithmetic or duplicate checks."""
    for key in REQUIRED_LINE_KEYS:
        if key not in line:
            return f"Line {number} is missing {key}"
    if not line["sku"]:
        return f"Line {number} must have a non-empty SKU"
    qty = _parse_integer(line["qty"])
    if qty is None:
        return f"Line {number} quantity must be an integer"
    if qty <= 0:
        return f"Line {number} quantity must be positive"
    price = _parse_integer(line["unit_price_kopecks"])
    if price is None:
        return f"Line {number} price must be an integer"
    if price < 0:
        return f"Line {number} price must be non-negative"
    return None


def validate_order(
    lines: list[dict[str, str]],
    promo_code: str = "",
    shipping_city: str = "",
) -> str | None:
    """Return a human readable reason why the order is invalid, or None if it is fine."""
    if promo_code and promo_code not in PROMO_CODES:
        return "Unknown promo code"
    if shipping_city and shipping_city not in SUPPORTED_CITIES:
        return "Unsupported shipping city"
    if not lines:
        return "Order must contain at least one line"
    seen_skus: set[str] = set()
    for number, line in enumerate(lines, start=1):
        reason = _validate_line(line, number)
        if reason is not None:
            return reason
        if line["sku"] in seen_skus:
            return f"Line {number} repeats SKU {line['sku']}"
        seen_skus.add(line["sku"])
    return None


def calculate_order_total(
    lines: list[dict[str, str]],
    promo_code: str = "",
    shipping_city: str = "",
) -> int | None:
    """Return the order total in kopecks, or None if the order is invalid."""
    ...
