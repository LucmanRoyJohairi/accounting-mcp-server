from datetime import datetime
from .repository import fetch_indexed_price_list


def calculate_line_audit(
    item_code: str | None,
    execution_date: str,
    billed_unit_price: float,
    quantity: float,
    billed_vat_rate: float,
    house_build_year: int | None = None,
    is_meerwerk: bool = False,
    meerwerk_approved_eur: float | None = None,
) -> dict:
    """Computes exact cent-rounded pricing, meerwerk cliff-edge (Art 4.5), and VAT (Art 4.6)."""
    billed_excl = round(billed_unit_price * quantity, 2)
    billed_vat_amt = round(billed_excl * billed_vat_rate, 2)
    billed_incl = round(billed_excl + billed_vat_amt, 2)

    if is_meerwerk:
        if meerwerk_approved_eur is not None:
            allowed_excl = round(min(billed_excl, float(meerwerk_approved_eur)), 2)
        elif billed_excl <= 250.00:
            allowed_excl = billed_excl
        else:
            allowed_excl = 0.00

        allowed_vat_rate = 0.21
        allowed_incl = round(allowed_excl * (1 + allowed_vat_rate), 2)
        return {
            "billed_excl": billed_excl,
            "allowed_excl": allowed_excl,
            "disputed_excl": round(billed_excl - allowed_excl, 2),
            "billed_vat_rate": billed_vat_rate,
            "expected_vat_rate": allowed_vat_rate,
            "billed_incl": billed_incl,
            "allowed_incl": allowed_incl,
            "disputed_incl": round(billed_incl - allowed_incl, 2),
        }

    price_list = {row["code"]: row for row in fetch_indexed_price_list()}
    if not item_code or item_code not in price_list:
        return {"error": f"Unknown item_code: {item_code}"}

    item = price_list[item_code]
    exec_dt = datetime.strptime(execution_date, "%Y-%m-%d")
    use_2026 = exec_dt >= datetime(2026, 1, 1)
    expected_unit_price = float(item["price_excl_vat_2026"] if use_2026 else item["price_excl_vat_2025"])

    expected_vat_rate = 0.21
    if item_code in ("W01", "W04") and house_build_year is not None:
        if (exec_dt.year - int(house_build_year)) > 2:
            expected_vat_rate = 0.09

    allowed_excl = round(expected_unit_price * quantity, 2)
    allowed_incl = round(allowed_excl * (1 + expected_vat_rate), 2)

    return {
        "pricing_year_applied": 2026 if use_2026 else 2025,
        "expected_unit_price": expected_unit_price,
        "billed_excl": billed_excl,
        "allowed_excl": allowed_excl,
        "disputed_excl": round(billed_excl - allowed_excl, 2),
        "billed_vat_rate": billed_vat_rate,
        "expected_vat_rate": expected_vat_rate,
        "billed_incl": billed_incl,
        "allowed_incl": allowed_incl,
        "disputed_incl": round(billed_incl - allowed_incl, 2),
    }
