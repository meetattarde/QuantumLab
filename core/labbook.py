"""Portable experiment records and session persistence for QUANTUM LAB."""
from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import json
import hashlib
from pathlib import Path
from typing import Any

import numpy as np

SCHEMA_VERSION = 1


@dataclass(frozen=True)
class RunRecord:
    """A compact, reproducible record of one plotted experiment run."""
    experiment: str
    parameters: dict[str, Any]
    created_utc: str
    summary: str
    metrics: dict[str, float]
    points: int


def curve_metrics(x, y) -> dict[str, float]:
    """Return generic scalar metrics for a finite one-dimensional curve."""
    x_values = np.asarray(x, dtype=float)
    y_values = np.asarray(y, dtype=float)
    if x_values.ndim != 1 or y_values.ndim != 1 or x_values.size != y_values.size:
        raise ValueError("Curve metrics require matching one-dimensional arrays.")
    if x_values.size < 2 or not np.all(np.isfinite(x_values)) or not np.all(np.isfinite(y_values)):
        raise ValueError("Curve metrics require at least two finite points.")
    maximum_index = int(np.argmax(y_values))
    return {
        "minimum": float(np.min(y_values)),
        "maximum": float(np.max(y_values)),
        "peak_x": float(x_values[maximum_index]),
        "area": float(np.trapezoid(y_values, x_values)),
    }


def make_record(experiment: str, parameters: dict[str, Any], result) -> RunRecord:
    """Build a record from QUANTUM LAB's standard experiment result tuple."""
    x, y, _, _, summary, _ = result
    if experiment == "Atomic orbitals":
        _, _, density = x
        metrics = {
            "minimum": float(np.min(density)),
            "maximum": float(np.max(density)),
            "mean": float(np.mean(density)),
        }
        points = int(np.asarray(density).size)
    else:
        metrics = curve_metrics(x, y)
        points = int(np.asarray(y).size)
    return RunRecord(
        experiment=experiment,
        parameters=dict(parameters),
        created_utc=datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        summary=str(summary),
        metrics=metrics,
        points=points,
    )


def save_session(path: str | Path, records: list[RunRecord], active_experiment: str, active_parameters: dict[str, Any]) -> None:
    """Write a versioned, human-readable session file."""
    payload = {
        "schema_version": SCHEMA_VERSION,
        "application": "QUANTUM LAB",
        "active_experiment": active_experiment,
        "active_parameters": active_parameters,
        "records": [asdict(record) for record in records],
    }
    canonical = json.dumps(payload, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    payload["integrity_sha256"] = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    Path(path).write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def load_session(path: str | Path) -> tuple[list[RunRecord], str, dict[str, Any]]:
    """Load and validate a session created by :func:`save_session`."""
    try:
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"Could not read session: {exc}") from exc
    if not isinstance(payload, dict) or payload.get("schema_version") != SCHEMA_VERSION:
        raise ValueError("Unsupported or invalid QUANTUM LAB session file.")
    supplied_digest = payload.pop("integrity_sha256", None)
    if supplied_digest is not None:
        canonical = json.dumps(payload, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
        expected_digest = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
        if supplied_digest != expected_digest:
            raise ValueError("Session integrity check failed. The file may have been changed or corrupted.")
    raw_records = payload.get("records", [])
    if not isinstance(raw_records, list):
        raise ValueError("Session records must be a list.")
    try:
        records = [RunRecord(**record) for record in raw_records]
    except (TypeError, ValueError) as exc:
        raise ValueError("Session contains an invalid experiment record.") from exc
    active_experiment = payload.get("active_experiment", "")
    active_parameters = payload.get("active_parameters", {})
    if not isinstance(active_experiment, str) or not isinstance(active_parameters, dict):
        raise ValueError("Session active experiment data is invalid.")
    return records, active_experiment, active_parameters
