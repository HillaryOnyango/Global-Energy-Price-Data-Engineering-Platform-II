from __future__ import annotations

from typing import Any


def parse_eia_payload(raw_document: dict[str, Any]) -> list[dict[str, Any]]:
    """Extract records from common EIA-style JSON shapes.

    Supports payload.data, payload.response.data, and raw list payloads.
    """
    payload = raw_document.get("payload", {})
    data = payload.get("data") if isinstance(payload, dict) else None
    if data is None and isinstance(payload, dict):
        data = payload.get("response", {}).get("data")
    if data is None and isinstance(payload, list):
        data = payload
    if data is None:
        data = []

    records: list[dict[str, Any]] = []
    for row in data:
        if not isinstance(row, dict):
            continue
        enriched = dict(row)
        enriched.setdefault("product_type", raw_document.get("product_type"))
        enriched.setdefault("source", raw_document.get("source"))
        enriched.setdefault("batch_id", raw_document.get("batch_id"))
        enriched.setdefault("ingestion_timestamp", raw_document.get("ingestion_timestamp"))
        records.append(enriched)
    return records
