# 🧾 Contract Audit (MCP Server)

A deterministic Model Context Protocol (MCP) server and AI audit skill built to automate monthly contractor invoice compliance checks for **Woonkring Oostervelde**.

It cross-references contractor invoices against the **2025–2027 Maintenance Framework Agreement (Article 4)**, master price lists, and work-order exports—flagging overcharges, calculating cent-exact variances, and generating dispute-ready audit dossiers.

---

## ✨ Key Capabilities

* 🧮 **Deterministic Financial Math:** Offloads all currency rounding, 2026 inflation indexation (`+3.2%`), and VAT splits (`9%` vs. `21%`) to Python rather than LLM estimation.
* 📄 **Multi-Contractor Parsing:** Normalizes inconsistent invoice layouts and Dutch date formats (`YYYY-MM-DD`, `DD-MM-YYYY`, `18 december 2025`) across all four maintenance partners (**Hoekstra**, **De Wit**, **Bosman**, and **Jansen**).
* ⚖️ **Article 4 Compliance Checks:**
  * 💰 **Art. 4.1 & 4.2 (Pricing & Indexation):** Validates unit rates against `price-agreement-2025.csv` and enforces the January 1, 2026 indexation boundary based on *execution date*.
  * 🚨 **Art. 4.3 (Call-Out Fees):** Restricts `voorrijkosten spoed` (`H06`, `B05`, `J05`) strictly to urgent (`spoed`) work orders (max once per order).
  * ⏱️ **Art. 4.4 (Labor Ceilings):** Enforces `max_labor_hours` unless pre-approved with a valid `MU-xxxx` token.
  * 🚧 **Art. 4.5 (Additional Work / Meerwerk):** Enforces the €250.00 unapproved threshold and full-rejection cliff edge (`> €250.00` without a `GA-xxxx` approval code).
  * 🏷️ **Art. 4.6 (Dual-Rate VAT):** Verifies `9%` VAT applies exclusively to painting labor (`W01`, `W04`) on properties older than 2 years.
  * 🔍 **Art. 4.8 & 4.9 (System Integrity):** Scans across all invoices to detect duplicate work-order billing, credit notes, and unknown work orders.
  * ✂️ **Art. 4.10 (Partial Payment Split):** Separates invoices into undisputed payable amounts and formal dispute amounts.

---

## 📁 Project Structure

```text
accounting-mcp-server/
├── server.py                             # FastMCP server & tool definitions
├── audit_engine/
│   ├── __init__.py
│   ├── parsers.py                        # Path-safe file reader, WO/credit/date extractors
│   ├── repository.py                     # CSV/JSON loaders & duplicate work-order scanner
│   └── calculator.py                     # Cent-exact Article 4 pricing, meerwerk & VAT math
├── .claude/
│   └── skills/
│       └── audit-invoices-skills.md      # Claude audit workflow & output schema
├── data/
│   ├── invoices/                         # Raw contractor invoice .txt files
│   ├── reference/
│   │   ├── contract-excerpt.md           # Original Dutch contract (Article 4)
│   │   ├── contract-excerpt-translated.md
│   │   ├── sanne-verdicts.csv            # Manual baseline verdicts (first 10 invoices)
│   │   ├── task-audit-transcript.md      # Discovery interview notes
│   │   └── translation-mapping.json      # Schema & Dutch business-term code mappings
│   ├── price-agreement-2025.csv          # Master 2025 contractor price list
│   └── work-orders-export.csv            # Work order database & approval tokens
├── requirements.txt
└── README.md
```

---

## 🚀 Setup & Installation

### 1. Clone & Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the MCP Server
```bash
python server.py
```

---

## 🛠️ Exposed MCP Tools

| Tool | Purpose |
| :--- | :--- |
| `list_invoice_files()` | Returns all invoice filenames in `data/invoices/` sorted alphabetically. |
| `check_duplicate_work_orders()` | Scans all invoices upfront to flag duplicate work orders and credit notes (Art. 4.8). |
| `read_invoice_content(filename)` | Safely reads an invoice and extracts contractor name, work order IDs, credit status, and normalized execution date. |
| `lookup_work_order(work_order_id)` | Retrieves work-order metadata (`job_type`, `maximum_hours_allowed`, `MU-xxxx`, `GA-xxxx`, `house_build_year`). |
| `get_indexed_price_list()` | Returns 2025 base rates alongside 2026 `+3.2%` indexed prices. |
| `get_contract_rules()` | Exposes static Article 4 thresholds and tax parameters. |
| `lookup_term_code(dutch_description, contractor)` | Maps Dutch line-item text to standardized contract codes (`H01`–`J05`). |
| `audit_invoice_line(...)` | Computes exact cent-rounded pricing, meerwerk cliff-edge penalties, and VAT splits. |

---

## 🛡️ Human-in-the-Loop Governance
This tool operates strictly as an **audit copilot**. It never authorizes payments or contacts contractors directly; all flagged variances require human review and sign-off before dispute notices are issued.
