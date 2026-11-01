# 📊 Invoice Audit Report: 10-File Sequential Pass

*  **Quick Status:** All 10 invoices are read and checked against their work orders, and the results are compiled below. The reference file `reference/Consultee-verdicts.csv` was missing from the environment during processing, leaving Section 3 blocked from automatic generation.

*  **Human-in-the-Loop Guardrail:** These findings represent proposed verdicts tailored specifically for Sanne’s sign-off. Nothing has been authorized, released, or sent to an external contractor.

---

## 📐 Scope & Method

*  **Target Scope:** While the macro skill outlines 40 total invoices, this execution pass was strictly limited to the 10 specific files you named, processed in your exact sequential order.

*  **VAT Treatment:** All calculated dispute amounts are inclusive of 21% VAT, which represents the real financial value Sanne would withhold at payment. Figures excluding VAT are isolated within the itemized calculations.

*  **Code Mapping Notes:** The mapping tool (`lookup_term_code`) returned no exact match for literal lines "Meerwerk: houtrot herstellen kozijn trapgat" or "Plafond sausen". These items were mapped manually against the framework price list (assigning code `W04` to the ceiling painting line). Additionally, all "Voorrijkosten spoed" strings map to code `B05` under Article 4.3 regardless of supplier.

---

## 📊 Section 1: Macro Financial Summary

*  **Total Invoices Processed:** 10

*  **Total Approved Payable Amount:** €14,209.66

*  **Total Amount to Dispute:** **€292.14** (Across 4 problem invoices)

*  **Invoices Placed on Hold:** 0

*  **Ledger Reconciliation Check:** Billed Total: €14,501.80. Balanced: Payable €14,209.66 + Disputed €292.14 = €14,501.80.

---

## 🗂️ Section 2: Detailed Line-Item Review List

### 1. `h-2026-0031.txt`
*  **Status:** Approved - Full Match 
*  **Contractor:** Hoekstra
*  **Work Order Associated:** `WO-26-1001` (Job Type: regulier)
*  **Audit Evidence:** 5 hours billed against an allowed maximum ceiling of 6 hours. Executed on 06-01-2026, meaning 2026 price indexation is correct. Totals and VAT allocations check out perfectly.
*  **Approved Payable Amount:** €3,424.60

***

### 2. `w-DW26-004.txt`
*  **Status:** Approved - Full Match
*  **Contractor:** De Wit Painters
*  **Work Order Associated:** `WO-26-1002` (Job Type: regulier)
*  **Audit Evidence:** 12 hours billed against an allowed maximum ceiling of 14 hours. Property build year is 1972, meaning the lower 9% VAT rate applied to labor (`W01`) and ceiling paint (`W04`) is legally valid. Standard paint materials billed at 21% are correct.
*  **Approved Payable Amount:** €1,213.87

***

### 3. `j-F26-0007.txt`
*  **Status:** Approved - Full Match
*  **Contractor:** Jansen
*  **Work Order Associated:** `WO-26-1003` (Job Type: spoed)
*  **Audit Evidence:** The travel call-out fee is permitted under Article 4.3 because the underlying work order is officially categorized as urgent (`spoed`), and it is billed only once. Labor is compliant at 2 hours billed against a 3-hour ceiling.
*  **Approved Payable Amount:** €255.99

***

### 4. `h-2026-0038.txt`
*  **Invoice File:** `h-2026-0038.txt`
*  **Contractor:** Hoekstra
*  **Work Order Associated:** `WO-26-1004`
*  **Proposed Status:** Dispute
*  **Undisputed Payable Amount:** €911.74
*  **Total Disputed Amount:** €29.17
*  **Itemized Deviations:**
    *   *Line Text:* "Radiator 600x1200 type 22"
    *   *Broken Contract Article:* Article 4.2 - Indexation applied to work executed in 2025
    *   *Evidence & Calculations:* Work was executed on "17-12-2025" but invoiced on 12-01-2026. Price indexation is prohibited because the physical work execution date sits prior to 01-01-2026.
        *   *Math:* Billed: 2 × €298.25 = €596.50 | Allowed (2025 price `H04`): 2 × €289.00 = €578.00 | Variance: €18.50
    *   *Line Text:* "Arbeid installateur"
    *   *Broken Contract Article:* Article 4.2 - Indexation applied to work executed in 2025
    *   *Evidence & Calculations:* Labor hours are structurally fine (3 hours billed against a 4-hour ceiling), but billed at incorrect 2026 indexed rates.
        *   *Math:* Billed: 3 × €60.37 = €181.11 | Allowed (2025 price `H02`): 3 × €58.50 = €175.50 | Variance: €5.61
    *   *Invoice-Level Calculation:* 
        *   *Total Excl. VAT:* €18.50 + €5.61 = €24.11
        *   *VAT 21% Leak:* €24.11 × 0.21 = €5.06
        *   *Total Leak Saved:* €24.11 + €5.06 = €29.17

***

### 5. `b-B-26-0102.txt`
*  **Invoice File:** `b-B-26-0102.txt`
*  **Contractor:** Bosman
*  **Work Order Associated:** `WO-26-1005`
*  **Proposed Status:** Dispute
*  **Undisputed Payable Amount:** €1,770.69
*  **Total Disputed Amount:** €56.19
*  **Itemized Deviations:**
    *   *Line Text:* "Voorrijkosten spoed"
    *   *Broken Contract Article:* Article 4.3 - Call-out fee on a regular work order
    *   *Evidence & Calculations:* Work order tracking fields show `job_type = "regulier"`. Travel call-out fees are strictly non-reimbursable for non-urgent tasks. The entire line item is rejected. Other labor lines are fine (6 hours billed against an 8-hour ceiling at valid 2026 rates).
        *   *Math:* Excl. VAT: 1 × €46.44 = €46.44 | VAT 21%: €46.44 × 0.21 = €9.75 | Total Dispute: €56.19

***

### 6. `w-DW26-009.txt`
*  **Status:** Approved - Full Match
*  **Contractor:** De Wit Painters
*  **Work Order Associated:** `WO-26-1006` (Job Type: regulier)
*  **Audit Evidence:** The extra work line "Meerwerk: houtrot herstellen kozijn trapgat" totals €385.00, which surpasses the standard €250.00 unapproved threshold. However, database verification reveals tracking code `GA-0412` is present, authorizing extra work up to a cap of €400.00. Because €385.00 ≤ €400.00, the line is fully valid under Article 4.5. Labor matches the strict 16-hour maximum ceiling perfectly. Reduced 9% VAT on labor is correct based on a 1968 property build year.
*  **Approved Payable Amount:** €1,486.38

***

### 7. `h-2026-0044.txt`
*  **Invoice File:** `h-2026-0044.txt`
*  **Contractor:** Hoekstra
*  **Work Order Associated:** `WO-26-1007`
*  **Proposed Status:** Dispute
*  **Undisputed Payable Amount:** €3,497.65
*  **Total Disputed Amount:** €146.10
*  **Itemized Deviations:**
    *   *Line Text:* "Arbeid installateur" (8 uur)
    *   *Broken Contract Article:* Article 4.4 - Hours above the work order maximum without an MU-xxxx approval
    *   *Evidence & Calculations:* The reference profile database restricts this task to a `maximum_hours_allowed` cap of 6. The work order contains no `MU-xxxx` override code to legitimize excess hours.
        *   *Math:* Disputed Overrun: 8 - 6 = 2 hours | Excl. VAT: 2 × €60.37 = €120.74 | VAT 21%: €120.74 × 0.21 = €25.36 | Total Dispute: €146.10

***

### 8. `w-DW26-011.txt`
*  **Invoice File:** `w-DW26-011.txt`
*  **Contractor:** De Wit Painters
*  **Work Order Associated:** `WO-26-1008`
*  **Proposed Status:** Dispute
*  **Undisputed Payable Amount:** €734.71
*  **Total Disputed Amount:** €60.68
*  **Itemized Deviations:**
    *   *Line Text:* "Arbeid schilder: 10 uur x EUR 50,57 = EUR 505,70 (21% btw)"
    *   *Broken Contract Article:* Article 4.6 - Wrong VAT rate on painting labor
    *   *Evidence & Calculations:* Property build year is 1968 and work execution occurred on 15-01-2026, meaning the building is older than 2 years. Painting labor (`W01`) qualifies for the reduced 9% tax exception. The contractor overbilled by applying standard 21% VAT to labor.
        *   *Math:* Correct Labor VAT (9%): €505.70 × 0.09 = €45.51 | Correct Paint VAT (21%): €151.65 × 0.21 = €31.85 | Correct Total VAT: €77.36 | Billed VAT: €138.04 | Variance Leak: €138.04 - €77.36 = €60.68
    *   *Sanne Judgment Call Flag:* The core skill text explicitly outlines the reverse case (billing 9% on a new build). This file over-bills VAT instead. The system applied Article 4.6 by symmetric logical extension. Please verify that this interpretation matches your operational intent.

***

### 9. `j-F26-0012.txt`
*  **Status:** Approved - Full Match
*  **Contractor:** Jansen
*  **Work Order Associated:** `WO-26-1009` (Job Type: regulier)
*  **Audit Evidence:** 2 hours billed against a 3-hour ceiling maximum. No travel call-out fees are billed to the account. Item base prices and mathematical VAT distributions check out cleanly on the document text.
*  **Approved Payable Amount:** €435.77

***

### 10. `b-B-26-0097.txt`
*  **Status:** Approved - Full Match
*  **Contractor:** Bosman
*  **Work Order Associated:** `WO-26-1010` (Job Type: spoed)
*  **Audit Evidence:** Travel call-out fee is fully allowed under Article 4.3 due to the urgent (`spoed`) categorization of the work order, and is only billed once. Labor is compliant at 3 hours billed against a 4-hour ceiling. Physical execution occurred on 03-01-2026, verifying that 2026 indexed contract prices are legitimate.
*  **Approved Payable Amount:** €478.26
