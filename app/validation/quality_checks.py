from __future__ import annotations

from collections import Counter
from dataclasses import asdict, dataclass, field
from typing import Any

import pandas as pd

from app.utils.constants import REQUIRED_FIELDS
from app.utils.ids import build_business_key

@dataclass
class ValidationResult:
    total_records: int
    valid_count: int
    invalid_count: int
    error_breakdown: dict[str, int] = field(default_factory=dict)
    sample_failing_records: list[dict[str, Any]] = field(default_factory=list)
    valid_records: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def validate_records(records: list[dict[str, Any]]) -> ValidationResult:
    errors = Counter()
    seen_keys: set[str] = set()
    valid_records = []
    failing_samples = []

    for record in records:
        record_errors = []

        for field in REQUIRED_FIELDS:
            if record.get(field) in (None, ""):
                record_errors.append(f"missing_{field}")

        price = pd.to_numeric(record.get("price"), errors="coerce")
        if pd.isna(price):
            record_errors.append("price_not_numeric")
        elif float(price) < 0:
            record_errors.append("negative_price")

        if pd.isna(pd.to_datetime(record.get("reporting_date"), errors="coerce", utc=True)):
            record_errors.append("invalid_reporting_date")

        business_key = record.get("business_key") or build_business_key(record)
        if business_key in seen_keys:
            record_errors.append("duplicate_business_key")
        seen_keys.add(business_key)

        if record_errors:
            errors.update(record_errors)
            if len(failing_samples) < 5:
                failing_samples.append({"record": record, "errors": record_errors})
        else:
            valid_records.append(record)

    return ValidationResult(
        total_records=len(records),
        valid_count=len(valid_records),
        invalid_count=len(records) - len(valid_records),
        error_breakdown=dict(errors),
        sample_failing_records=failing_samples,
        valid_records=valid_records,
    )
