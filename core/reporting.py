"""Human-readable research-report export for saved QUANTUM LAB sessions."""
from __future__ import annotations

from pathlib import Path
from typing import Iterable

from core.labbook import RunRecord


def format_report(records: Iterable[RunRecord], active_experiment: str) -> str:
    records = list(records)
    lines = [
        "# QUANTUM LAB — Session Report",
        "",
        f"Active experiment: **{active_experiment}**",
        f"Recorded runs: **{len(records)}**",
        "",
        "## Scope",
        "This report documents outputs from educational numerical models. It is not a substitute for measured experimental data or a quantified uncertainty analysis.",
        "",
    ]
    if not records:
        lines.append("No runs were recorded in this session.")
    for index, record in enumerate(records, 1):
        lines.extend([f"## Run {index}: {record.experiment}", "", f"Recorded (UTC): {record.created_utc}", "", "### Parameters"])
        lines.extend(f"- `{key}`: {value}" for key, value in record.parameters.items())
        lines.extend(["", "### Derived metrics"])
        lines.extend(f"- {key}: {value:.8g}" for key, value in record.metrics.items())
        lines.extend(["", "### Model summary", record.summary, ""])
    return "\n".join(lines)


def save_report(path: str | Path, records: Iterable[RunRecord], active_experiment: str) -> None:
    Path(path).write_text(format_report(records, active_experiment), encoding="utf-8")
