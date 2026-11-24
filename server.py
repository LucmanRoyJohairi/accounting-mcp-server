from fastmcp import FastMCP
from audit_engine.parsers import (
    safe_invoice_path,
    extract_work_orders,
    is_credit_note,
    parse_dutch_execution_date,
)
from audit_engine.repository import (
    INVOICES_DIR,
    MAPPING,
    get_invoice_filenames,
    find_duplicate_work_orders,
    fetch_work_order,
    fetch_indexed_price_list,
    resolve_term_code,
)
from audit_engine.calculator import calculate_line_audit

mcp = FastMCP("OosterveldeInvoiceAuditor")


@mcp.tool()
def list_invoice_files() -> list[str]:
    """Lists all available invoice filenames sorted alphabetically."""
    return get_invoice_filenames()


@mcp.tool()
def check_duplicate_work_orders() -> dict:
    """Scans all invoices to detect duplicate work orders across files (Article 4.8)."""
    return find_duplicate_work_orders()


@mcp.tool()
def read_invoice_content(filename: str) -> dict:
    """Reads raw invoice text safely and extracts contractor, work orders, credit status, and execution date."""
    safe_path = safe_invoice_path(INVOICES_DIR, filename)
    if not safe_path:
        return {"error": f"Invalid or missing invoice: {filename}"}

    with open(safe_path, "r", encoding="utf-8") as f:
        content = f.read()

    detected_wos = extract_work_orders(content)
    fn_lower = filename.lower()
    prefixes = MAPPING.get("contractor_prefixes", {})
    contractor = next((name for p, name in prefixes.items() if fn_lower.startswith(p)), None)

    return {
        "filename": filename,
        "detected_contractor": contractor,
        "detected_work_orders": detected_wos,
        "detected_work_order": next(iter(detected_wos), None),
        "detected_execution_date": parse_dutch_execution_date(content),
        "is_credit_note": is_credit_note(content),
        "raw_text": content,
    }


@mcp.tool()
def lookup_work_order(work_order_id: str) -> dict:
    """Looks up specific work order parameters with normalized columns."""
    return fetch_work_order(work_order_id)


@mcp.tool()
def get_indexed_price_list() -> list[dict]:
    """Returns the 2025 master price list alongside the 3.2% 2026 inflation-adjusted prices."""
    return fetch_indexed_price_list()


@mcp.tool()
def get_contract_rules() -> dict:
    """Returns static framework compliance constraints derived from Article 4."""
    return {
        "price_indexation_modifier": 0.032,
        "indexation_effective_date": "2026-01-01",
        "emergency_callout_allowed_type": "spoed",
        "regular_callout_allowed": False,
        "unapproved_meerwerk_cap_eur": 250.00,
        "historical_invoice_registry_path": "data/invoices",
        "vat_standard_rate": 0.21,
        "vat_historical_labor_rate": 0.09,
        "vat_historical_labor_age_threshold_years": 2,
    }


@mcp.tool()
def lookup_term_code(dutch_description: str, contractor: str | None = None) -> dict:
    """Resolves Dutch invoice descriptions into operational item codes."""
    return resolve_term_code(dutch_description, contractor)


@mcp.tool()
def audit_invoice_line(
    item_code: str | None,
    execution_date: str,
    billed_unit_price: float,
    quantity: float,
    billed_vat_rate: float,
    house_build_year: int | None = None,
    is_meerwerk: bool = False,
    meerwerk_approved_eur: float | None = None,
) -> dict:
    """Performs exact cent-rounded math for line pricing, meerwerk cliff-edge, and VAT."""
    return calculate_line_audit(
        item_code=item_code,
        execution_date=execution_date,
        billed_unit_price=billed_unit_price,
        quantity=quantity,
        billed_vat_rate=billed_vat_rate,
        house_build_year=house_build_year,
        is_meerwerk=is_meerwerk,
        meerwerk_approved_eur=meerwerk_approved_eur,
    )


if __name__ == "__main__":
    mcp.run()
