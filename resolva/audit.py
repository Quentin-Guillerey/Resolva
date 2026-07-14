"""
Audit log — append-only CSV, written for every SME decision and every
auto-publish (approvals and rejections both leave a row).

Reuses the toolkit's CSV audit structure, with the columns Resolva's spec
requires. The CSV lives in the per-user data directory, separate from the
SQLite knowledge base, so the trail is a plain, portable, append-only
file an auditor can open in Excel without touching the app.

A failed audit write raises: for an audit-ready tool, silently continuing
without the trail would be worse than stopping the operator.
"""

import csv
from datetime import datetime
from .config import audit_path

COLUMNS = [
    "Ticket Number",
    "Date",
    "Account Number",       # sanitized internal 6-digit
    "Description",
    "Resolution",
    "Time to Resolve",
    "Stakeholders Involved",
    "Validation Process",   # auto | manual
    "Additional Comments",
]


def write_audit(row: dict) -> None:
    path = audit_path()
    exists = path.exists()
    record = [
        row.get("ticket_number", ""),
        row.get("date") or datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        row.get("account_number", ""),
        row.get("description", ""),
        row.get("resolution", ""),
        row.get("time_to_resolve", ""),
        row.get("stakeholders", ""),
        row.get("validation_process", ""),
        row.get("comments", ""),
    ]
    with open(path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not exists:
            writer.writerow(COLUMNS)
        writer.writerow(record)


def read_audit() -> list:
    """Return the audit log as a list of dict rows (newest first) for display."""
    path = audit_path()
    if not path.exists():
        return []
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    return list(reversed(rows))
