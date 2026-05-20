from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

import pandas as pd

from app.utils.ids import build_business_key

FIELD_ALIASES = {
    "country": ["country", "country_name", "area-name", "area_name", "region"],
    "price": ["price", "value", "amount"],
    "currency": ["currency", "currency_code"],
    "unit": ["unit", "units"],
    "reporting_date": ["reporting_date", "period", "date", "timestamp"],
}

PRODUCT_MAP = {
    "gasoline": "fuel",
    "diesel": "fuel",
    "fuel": "fuel",
    "electricity": "electricity",
    "power": "electricity",
    "natural gas": "natural_gas",
    "natural_gas": "natural_gas",
    "gas": "natural_gas",
}


def _first_value(row: dict[str, Any], aliases: list[str]) -> Any:
    for key in aliases:
        if key in row and row[key] not in (None, ""):
            return row[key]
    return None


def normalize_record(row: dict[str, Any]) -> dict[str, Any]:
    product_raw = str(row.get("product_type") or row.get("product") or "").strip().lower()
    product_type = PRODUCT_MAP.get(product_raw, product_raw or "unknown")

    reporting_date = _first_value(row, FIELD_ALIASES["reporting_date"])
    parsed_date = pd.to_datetime(reporting_date, errors="coerce", utc=True)

    record = {
        "country": _first_value(row, FIELD_ALIASES["country"]),
        "product_type": product_type,
        "price": pd.to_numeric(_first_value(row, FIELD_ALIASES["price"]), errors="coerce"),
        "currency": _first_value(row, FIELD_ALIASES["currency"]) or "USD",
        "unit": _first_value(row, FIELD_ALIASES["unit"]) or "unknown",
        "reporting_date": None if pd.isna(parsed_date) else parsed_date.to_pydatetime(),
        "source": row.get("source", "EIA_API"),
        "ingestion_timestamp": row.get("ingestion_timestamp") or datetime.now(timezone.utc).isoformat(),
        "batch_id": row.get("batch_id"),
        "raw_record": row,
    }
    record["business_key"] = build_business_key(record)
    return record


def normalize_records(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [normalize_record(row) for row in rows]
