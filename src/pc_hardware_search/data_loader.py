from __future__ import annotations

import csv
from pathlib import Path

from .models import Part


def _parse_optional_int(value: str) -> int | None:
    value = value.strip()
    return int(value) if value else None


def _parse_optional_str(value: str) -> str | None:
    value = value.strip()
    return value if value else None


def load_parts(csv_path: str | Path) -> list[Part]:
    parts: list[Part] = []
    with open(csv_path, newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            parts.append(
                Part(
                    category=row["category"].strip(),
                    model=row["model"].strip(),
                    price=float(row["price"]),
                    score=float(row["score"]),
                    socket=_parse_optional_str(row.get("socket", "")),
                    tdp_watts=_parse_optional_int(row.get("tdp_watts", "")),
                    ram_type=_parse_optional_str(row.get("ram_type", "")),
                    memory_gb=_parse_optional_int(row.get("memory_gb", "")),
                )
            )
    return parts
