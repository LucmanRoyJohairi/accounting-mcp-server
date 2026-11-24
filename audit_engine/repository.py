import os
import json
import re
import pandas as pd
from .parsers import extract_work_orders, is_credit_note

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
INVOICES_DIR = os.path.abspath(os.path.join(DATA_DIR, "invoices"))


def load_mapping() -> dict:
    path = os.path.join(DATA_DIR, "reference", "translation-mapping.json")
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


MAPPING = load_mapping()


def get_invoice_filenames() -> list[str]:
    if not os.path.exists(INVOICES_DIR):
        return []
    return sorted(
        f for f in os.listdir(INVOICES_DIR)
        if os.path.isfile(os.path.join(INVOICES_DIR, f))
    )


def find_duplicate_work_orders() -> dict:
    wo_map: dict[str, list[dict]] = {}
    for filename in get_invoice_filenames():
        with open(os.path.join(INVOICES_DIR, filename), "r", encoding="utf-8") as f:
            content = f.read()

        credit = is_credit_note(content)
        for wo in extract_work_orders(content):
            wo_map.setdefault(wo, []).append({"filename": filename, "is_credit_note": credit})

    duplicates = {wo: files for wo, files in wo_map.items() if len(files) > 1}
    return {"duplicate_count": len(duplicates), "duplicates": duplicates}


def fetch_work_order(work_order_id: str) -> dict:
    path = os.path.join(DATA_DIR, "work-orders-export.csv")
    if not os.path.exists(path):
        return {"error": "Work order database file missing."}

    df = pd.read_csv(path)
    row = df[df["wo"] == work_order_id]
    if row.empty:
        return {"error": f"Work order {work_order_id} not found."}

    record = row.to_dict(orient="records").pop(0)
    col_map = MAPPING.get("csv_columns", {})
    return {
        col_map.get(k, k): (None if pd.isna(v) else v)
        for k, v in record.items()
    }




def fetch_indexed_price_list() -> list[dict]:
    path = os.path.join(DATA_DIR, "price-agreement-2025.csv")
    if not os.path.exists(path):
        return []

    df = pd.read_csv(path)
    df["price_excl_vat_2026"] = (df["price_excl_vat_2025"] * 1.032).round(2)
    df = df.where(pd.notnull(df), None)
    return df.to_dict(orient="records")


def resolve_term_code(dutch_description: str, contractor: str | None = None) -> dict:
    clean_desc = dutch_description.strip().lower()
    terms = MAPPING.get("business_terms", {})
    prefix_map = {"hoekstra": "H", "de wit": "W", "bosman": "B", "jansen": "J"}
    target_prefix = prefix_map.get(contractor.strip().lower()) if contractor else None

    def _pick(val):
        if isinstance(val, list):
            if target_prefix:
                return next((c for c in val if c.startswith(target_prefix)), val)
            return val
        return val

    if clean_desc in terms:
        return {"matched": True, "code": _pick(terms[clean_desc])}

    for key, val in terms.items():
        if len(key) >= 4 and re.search(rf"\b{re.escape(key)}\b", clean_desc):
            return {"matched": True, "code": _pick(val)}

    return {"matched": False, "code": None}
