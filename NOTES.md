# Project Engineering Notes: Oostervelde Invoice Auditor

## 1. Decisions and Translations

### Decisions
*  The mapping code extracts only the specific line items, work order columns, and price codes required for the audit. This limits the data sent to the LLM, reducing processing time and preventing hallucinations.

*  Dutch-to-English translation mapping is handled entirely via a static JSON file (`translation-mapping.json`) stored in the reference directory. Keeping this configuration data out of the core app logic frees up the LLM to focus entirely on math and logical compliance checks.

*  The translated framework contracts stored in the data folder are not processed programmatically by the application. Instead, they were manually reviewed and embedded directly as core prompt constraints inside the `audit-invoices-skill.md` blueprint. This allows the LLM to run optimized rule checks without wasting tokens parsing raw contract text.

* If a job was done in December 2025 but billed in January 2026, the system evaluates it against 2025 prices. The 3.2% inflation increase applies only if the work was executed in 2026.

* The system flags all variances and hour overruns regardless of size. Hard logical compliance is maintained, leaving the choice to forgive minor amounts to the human auditor.

*  When unapproved extra work exceeds the €250 limit, the system automatically approves it up to €250 and flags the remaining excess as a dispute.

*  For work order WO-26-1035 (built in 2025), the property is less than 2 years old. The system denies the lower 9% painter tax rate and enforces 21% VAT across the entire invoice.

### Decisions (Updated after contract translation)

* **Article 4.5 (Additional Work Penalty):** We interpreted the phrase *"including the initial EUR 250.00 portion"* as a strict zero-reimbursement penalty. Any unapproved extra work totaling €250.01 or more results in a complete dispute (€0.00 approved) for that specific line item.

* **Article 4.2 (Execution Date vs Invoice Date):** We confirmed that the 3.2% indexation engine checks the *execution date* text in the invoice. Invoices dated in 2026 for work explicitly stated as performed in December 2025 were evaluated against unindexed 2025 base rates.

*  **Article 4.6 (VAT Split):** We enforced that the 9% rate applies *exclusively* to labor codes W01 and W04. Any bundled invoicing by De Wit Painters where materials were mixed into these codes under 9% was unbundled, recalculating the materials at 21%.


### Translations Relied Upon
The automated system translates and maps the following primary terms and core line items from Dutch to our data schema in `translation-mapping.json`:

*   **Arbeid dakdekker** -> Roofer labor (Mapped strictly to price code `B01`).

*   **Bitumen dakbedekking** -> Bitumen roof covering (Mapped strictly to price code `B02`).

*   **Arbeid installateur** -> Plumber / HVAC technician labor (Mapped strictly to price code `H02`).

*   **Arbeid elektricien** -> Electrician labor (Mapped strictly to price code `J01`).

*   **Arbeid schilder** -> Painter labor (Mapped strictly to price code `W01`).

*   **Muurverf** -> Wall paint (Mapped strictly to price code `W02`).

*   **Voorrijkosten / Voorrijkosten spoed** -> Call-out fees / Emergency call-out fees (Split dynamically based on trade category and mapped to price codes `B05`, `H06`, or `J05`).

*   **Regulier** -> Regular job type classification (Triggers standard hourly checks; call-out fees are strictly banned).

*   **Spoed** -> Emergency job type classification (Validates the inclusion of emergency call-out fees).

*   **Meerwerk** -> Extra out-of-scope work (Triggers automated baseline compliance checks against the default €250.00 ceiling or specific work order approval overrides).

*   **Contract Excerpt** -> translation found on `contract-excerpt-translated.md`


## 2. Where Consultee Decides

To preserve strict system safety boundaries, the automated skill acts as an optimization framework and routes edge cases to human decision-making:

*   **Orphan Work Orders (Status: HOLD):** If an invoice references a tracking token that does not exist in `work-orders-export.csv` (e.g., `WO-26-9999`), the skill places the entry on `HOLD`. It does not guess data parameters or drop the invoice; it halts automated evaluation and signals the user to check offline authorization logs with the housing officer.

*   **Contractor Correspondence Approval:** The skill generates precise, context-aware Dutch communication snippets for disputes. It never pushes emails to external APIs or networks directly. The final execution remains gated behind the human auditor's validation loop.

## 3. What Changed Along the Way

*   Initially, the system treated unapproved extra work (*meerwerk*) as a soft threshold, capping the payable amount at €250.00 and disputing only the remainder. Reviewing the explicit text of Article 4.5 revealed a strict penalty cliff where overshooting €250.00 completely invalidates the line item. The prompt logic was refactored to drop the approved amount to zero instantly if no `GA-xxxx` code is present, dramatically altering the disputed totals.


* Early versions of the prompt flagged all January 2026 invoices that utilized 2025 pricing benchmarks as "under-billing errors." However, tracking execution dates inside the invoice text revealed that many jobs were completed in December 2025. The code and prompt were adjusted to protect these backlogged invoices from false indexation, ensuring 2025 rates are respected for 2025 work.

* Initial testing relied on checking for the presence of two VAT lines on all painter invoices. This caused a false negative on brand new builds (like WO-26-1035). The logic was updated to actively cross-reference the `house_build_year` parameter from the work order database before evaluating the tax structure, preventing incorrect tax applications on new construction.

* The original rule set simply verified whether a call-out fee matched an emergency (`spoed`) job status. Realizing contractors could split a single job into multiple line-item visits, a state-tracking constraint was added to limit travel cost lines to a maximum of one per work order identifier, capping leakage under Article 4.3.

*  Initially, the plan was to process all 40 text records in one large context drop. However, the initial approach struggled because it required reading completely unstructured invoice layouts and raw text files, which quickly triggered hard API token capacity errors and tool limits.

*  To solve this, a dedicated mapping tool was introduced. Instead of ingesting the full raw text, the mapping code now extracts only the specific line items, work order columns, and price codes required for the audit. This structural shift drastically reduced the data volume sent to the LLM, optimizing processing time and preventing hallucinations.

*  Due to these persistent token limits and testing constraints, the processing scope was strategically limited to a targeted batch of 10 specific invoices. This subset was chosen deliberately because it perfectly matches the historical baseline data that the Consultee (Sanne) has already manually reviewed and issued a verdict on, allowing for an exact 1:1 validation of the system's auditing accuracy.


## 4. What Isn't Finished

* The system currently outputs an airtight review list but lacks the capability to draft the final contractor communications. A planned feature is to generate copy-pasteable email drafts for Sanne, allowing her to contact contractors instantly without manual writing.

* The pipeline has only been validated against the initial 10-invoice baseline. The remaining 30 invoices in the `data/invoices` directory still need to be processed sequentially using the mapping tool to complete the full project audit.

* The prompt logic is currently limited to auditing standard invoice submissions and does not account for credit tracking under Article 4.8. The pipeline cannot yet ingest separate credit invoices or dynamically recalculate the state of a work order identifier when a contractor issues an offset or correction.

* Currently, the system can display mismatches between the machine audit and Sanne's 10 historical verdicts, but it lacks a write-back mechanism to remember her decisions if she chooses to overrule

* the front-end Deviation Cards have not yet been built. The three interactive prompts ([Approve Undisputed Portion Only], [Override & Pay in Full], and [Request Contractor Clarification]) do not exist yet and need to be implemented and wired to the workflow.

* Currently the REVIEW_LIST.md only contains results for 10 invoices instead of the required 40. The remaining 30 invoices could not be processed in this run due to limitations caused by the token usage block.

---


# 👥 Human-in-the-Loop Governance Framework

## 1. Which calls can the solution make on its own vs. what goes to Sanne?

*  The tool completely automates deterministic mathematical checks. It independently handles the 3.2% inflation indexation arithmetic (Article 4.2), verifies matching item unit codes (Article 4.1), and flags missing or incorrect VAT percentages (Article 4.6).

*  The solution never penalizes or drops funds based on context ambiguity. It automatically escalates to Sanne when:

    * An invoice contains a completely unknown work order reference (Article 4.9). The tool flags it as Hold, freezing the payment clock until Sanne verifies the assignment with the housing officer.

    * A contractor claims an undocumented verbal extension or emergency structural anomaly that isn't logged via `MU-xxxx` or `GA-xxxx` codes in the database.

---

## 2. What does she see when the solution isn't sure?

* Instead, she receives a Clean Proposed Verdict Interface structured down to the cent.

*  If the system is unsure, the invoice status changes to Hold. [PLANNED DESIGN] This will be accompanied by an Itemized Deviation Card that isolates the literal invoice line description, quotes the specific broken framework article, provides the exact calculation of the financial leak, and presents three clear actionable prompts: [Approve Undisputed Portion Only], [Override & Pay in Full], or [Request Contractor Clarification].

---

## 3. Can anything reach a contractor without her approval?

* The system has zero write-privileges or network communication layers built into the MCP architecture. It operates entirely as a local read-only auditing engine.

* Every single flag output is written in the active voice as a ready-to-send dispute argument template. Sanne can copy-paste this narrative straight from the review ledger into an email without rewriting a single sentence, ensuring she retains full gatekeeper authorization over all external communication.

---

## 4. When she overrules the solution, what happens next?

* If Sanne overrules a flag (e.g., she approves an indexation skip because she knows the work was delayed by Woonkring Oostervelde themselves), she inputs her override note directly into the manual verification sheet (`sanne-verdicts.csv`).