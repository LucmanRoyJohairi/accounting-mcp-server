## Section 3: Variance Comparison Report (First 10 Invoices)

*  **Overall Result:** 8 of 10 verdicts match on status (approve or dispute). There are 2 status mismatches and 1 amount difference on an invoice where we agree on the status.

| # | Invoice | Sanne | Mine | Match |
|---|---|---|---|---|
| 1 | `h-2026-0031.txt` | approve | approve | ✅ |
| 2 | `w-DW26-004.txt` | approve | approve | ✅ |
| 3 | `j-F26-0007.txt` | approve | approve | ✅ |
| 4 | `h-2026-0038.txt` | approve | dispute €29.17 | ❌ |
| 5 | `b-B-26-0102.txt` | dispute | dispute €56.19 | ✅ status, ⚠️ amount |
| 6 | `w-DW26-009.txt` | dispute | approve | ❌ |
| 7 | `h-2026-0044.txt` | dispute (2h) | dispute (2h, €146.10) | ✅ |
| 8 | `w-DW26-011.txt` | dispute (9% VAT) | dispute €60.68 | ✅ |
| 9 | `j-F26-0012.txt` | approve | approve | ✅ |
| 10 | `b-B-26-0097.txt` | approve | approve | ✅ |

---

### Mismatch 1: `h-2026-0038.txt` (I caught it, Sanne approved)

*  **Who caught what:** I disputed the indexation on a job executed in 2025. Sanne approved it.

*  **Why the gap occurred:** Sanne’s note says "prijzen kloppen met de nieuwe prijslijst" (prices match the new price list). The invoice does bill at the 2026 prices, so checking against that list looks correct on the surface. But the invoice is dated 12-01-2026, while the work was executed on "17-12-2025".

*  **Contract Resolution:** Article 4.2 resolves it. Indexation applies only when the execution date is on or after 01-01-2026, not the invoice date. The 2025 prices apply here.
   * Radiators: €596.50 - €578.00 = €18.50
   * Labor: €181.11 - €175.50 = €5.61
   * Excl. VAT: €18.50 + €5.61 = €24.11
   * Incl. VAT 21%: €24.11 + €5.06 = €29.17

*  **Proposed reconciliation:** My dispute stands. This is the classic invoice-date versus execution-date trap the skill warns about.

---

### Mismatch 2: `w-DW26-009.txt` (Sanne disputed, I approved)

*  **Who caught what:** Sanne disputed the extra work. I approved it.

*  **Why the gap occurred:** Sanne’s note says "meerwerk 385,00 boven de 250, geen akkoord gezien". She is right that €385.00 exceeds the €250.00 threshold, and that would trigger the cliff-edge rejection under Article 4.5. But the work order `WO-26-1006` records approval code `GA-0412` for €400.00.

*  **Contract Resolution:** Article 4.5 resolves it. Extra work above €250.00 is reimbursable up to the approved amount when a valid `GA-xxxx` code exists.
   * Billed: €385.00
   * Approved cap: €400.00
   * Evaluation: €385.00 ≤ €400.00, so the line is payable in full.

*  **Likely cause:** The invoice text doesn’t mention `GA-0412`. The code appears only in the work order record, so it is easy to miss if you check the invoice alone.

*  **Proposed reconciliation:** I’d approve. Because this reverses Sanne’s call, please confirm in the source system that `GA-0412` is real and approved before releasing payment.

*  **Exposure if Sanne is right:** The whole €385.00 would be rejected. Incl. VAT: €385.00 × 1.21 = €465.85.

---

### Amount difference: `b-B-26-0102.txt` (Same status, different figure)

*  **Who caught what:** We both caught the call-out fee on a regular work order (Article 4.3). Sanne’s note says to reclaim "45,00 + btw".

*  **Why the figures differ:** €45.00 is the 2025 base price for `B05`. The invoice actually billed €46.44, the indexed price, and the work was executed on 12-01-2026, so the indexed price is legitimate for that date.

*  **Contract Resolution:** Article 4.3 resolves it. The entire line item amount is disputed, so the dispute equals what was billed.
   * Mine: €46.44 + €9.75 VAT = €56.19
   * Sanne’s: €45.00 + €9.45 VAT = €54.45
   * Difference: €56.19 - €54.45 = €1.74

*  **Proposed reconciliation:** Reclaim €56.19. Reclaiming only €45.00 would leave €1.74 of non-reimbursable cost paid.

---

### Matches worth noting

*  **`w-DW26-011.txt`:** Sanne confirms that painting labor billed at 21% should be 9%. This settles the judgment call I flagged earlier about the VAT direction. My figure is €60.68; her note gives no amount.

*  **`h-2026-0044.txt`:** We agree on 2 excess hours. I put it at €120.74 excl. VAT, or €146.10 incl. VAT. Her note gives no amount.

---

### Net effect on the totals

*  **My totals:** €292.14 disputed, €14,209.66 payable.

*  **Sanne's totals (If used instead):** About €727.08 disputed, which is a different picture driven mostly by the `GA-0412` question.
   * Calculation: €54.45 + €465.85 + €146.10 + €60.68 = €727.08
   * Note: This figure uses her €45.00 for `b-B-26-0102` and rejects the full extra-work line on `w-DW26-009`.

*  **Core Takeaway:** **The single item that moves the total most is `w-DW26-009`, so confirming `GA-0412` is the most valuable check before sign-off.**
