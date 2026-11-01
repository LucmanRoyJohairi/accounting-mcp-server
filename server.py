import os
import json
import re
import pandas as pd
from fastmcp import FastMCP

# Initialize FastMCP Server
mcp = FastMCP("OosterveldeInvoiceAuditor")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

# 1. Deterministic Mapping Cache
def load_mapping():
    mapping_path = os.path.join(DATA_DIR, "reference", "translation-mapping.json")
    if os.path.exists(mapping_path):
        with open(mapping_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

MAPPING = load_mapping()

# --- ATOMIC TOOLS ---

@mcp.tool()
def list_invoice_files() -> list[str]:
    """Lists all available invoice filenames from the invoices directory."""
    folder = os.path.join(DATA_DIR, "invoices")
    if not os.path.exists(folder):
        return []
    return [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]

@mcp.tool()
def read_invoice_content(filename: str) -> dict:
    """Reads raw invoice text securely with strict local prefix identification."""
    path = os.path.join(DATA_DIR, "invoices", filename)
    if not os.path.exists(path):
        return {"error": f"Invoice {filename} not found."}
    
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # 1. Deterministic work order token scanning
    wo_match = re.search(r"WO-26-\d{4}", content)
    detected_wo = wo_match.group(0) if wo_match else None
    
    # 2. NEW: Deterministic Contractor Identification via Filename Pattern
    fn_lower = filename.lower()
    contractor_mapping = {
        "b-": "Bosman",
        "h-": "Hoekstra",
        "j-": "Jansen",
        "w-": "De Wit"
    }
    
    detected_contractor = None
    for prefix, contractor in contractor_mapping.items():
        if fn_lower.startswith(prefix):
            detected_contractor = contractor
            break
        
    return {
        "filename": filename,
        "detected_contractor": detected_contractor, # Clean parameter for Claude!
        "detected_work_order": detected_wo,
        "raw_text": content
    }


@mcp.tool()
def lookup_work_order(work_order_id: str) -> dict:
    """Looks up specific work order parameters with normalized columns."""
    path = os.path.join(DATA_DIR, "work-orders-export.csv")
    if not os.path.exists(path):
        return {"error": "Work order database file missing."}
    
    df = pd.read_csv(path)
    row = df[df["wo"] == work_order_id]
    if row.empty:
        return {"error": f"Work order {work_order_id} not found."}
    
    data = row.iloc[0].to_dict()
    
    # Map raw columns to clear schema terms via translation-mapping
    mapped_data = {}
    col_map = MAPPING.get("csv_columns", {})
    for key, val in data.items():
        new_key = col_map.get(key, key)
        # Convert NaN values to None for clean JSON compliance
        mapped_data[new_key] = None if pd.isna(val) else val
        
    return mapped_data

@mcp.tool()
def get_indexed_price_list() -> list[dict]:
    """Returns the 2025 master price list instantly indexed with the 3.2% 2026 inflation modifier."""
    path = os.path.join(DATA_DIR, "price-agreement-2025.csv")
    if not os.path.exists(path):
        return []
    
    df = pd.read_csv(path)
    # Apply deterministic indexation to clean numbers instantly
    df["price_excl_vat_2026"] = (df["price_excl_vat_2025"] * 1.032).round(2)
    return df.to_dict(orient="records")

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
        "vat_historical_labor_age_threshold_years": 2
    }

@mcp.tool()
def lookup_term_code(dutch_description: str) -> dict:
    """Resolves raw Dutch invoice strings directly into unified operational item codes."""
    clean_desc = dutch_description.strip().lower()
    terms = MAPPING.get("business_terms", {})
    
    # Direct dictionary check
    if clean_desc in terms:
        return {"matched": True, "code": terms[clean_desc]}
        
    # Fallback fuzzy substring scan
    for key, code in terms.items():
        if key in clean_desc or clean_desc in key:
            return {"matched": True, "code": code}
            
    return {"matched": False, "code": None}

if __name__ == '__main__':
    mcp.run()
