import os
import re

DUTCH_MONTHS = {
    "januari": "01", "februari": "02", "maart": "03", "april": "04",
    "mei": "05", "juni": "06", "juli": "07", "augustus": "08",
    "september": "09", "oktober": "10", "november": "11", "december": "12"
}


def safe_invoice_path(invoices_dir: str, filename: str) -> str | None:
    """Resolves an invoice path and blocks directory traversal."""
    safe_path = os.path.abspath(os.path.join(invoices_dir, filename))
    if not safe_path.startswith(invoices_dir + os.sep) or not os.path.isfile(safe_path):
        return None
    return safe_path


def extract_work_orders(content: str) -> list[str]:
    """Finds all unique WO-26-XXXX tokens in invoice text."""
    return sorted(set(re.findall(r"WO-26-\d{4}", content)))


def is_credit_note(content: str) -> bool:
    """Checks whether the document is a credit invoice."""
    return bool(re.search(r"\bcredit(?:factuur|nota)?\b", content, re.I))


def parse_dutch_execution_date(content: str) -> str | None:
    """Normalizes execution dates across all 4 contractor formats to YYYY-MM-DD."""
    m_iso = re.search(r"(?:uitvoeringsdatum|uitgevoerd|datum uitvoering)[^\d]*(\d{4}-\d{2}-\d{2})", content, re.I)
    if m_iso:
        return m_iso.group(1)

    m_dmy = re.search(r"(?:uitvoeringsdatum|uitgevoerd|datum uitvoering)[^\d]*(\d{2})[-/](\d{2})[-/](\d{4})", content, re.I)
    if m_dmy:
        day, month, year = m_dmy.groups()
        return f"{year}-{month}-{day}"

    months_pattern = "|".join(DUTCH_MONTHS.keys())
    m_nl = re.search(
        rf"(?:uitvoeringsdatum|uitgevoerd|datum uitvoering)[^\d]*(\d{{1,2}})\s+({months_pattern})\s+(\d{{4}})",
        content,
        re.I,
    )
    if m_nl:
        day, month_name, year = m_nl.groups()
        return f"{year}-{DUTCH_MONTHS[month_name.lower()]}-{int(day):02d}"

    return None
