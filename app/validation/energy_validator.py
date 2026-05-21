from collections import Counter
from datetime import datetime, timezone

from app.utils.logger import get_logger

logger = get_logger(__name__)


REQUIRED_FIELDS = [
    "period",
    "area-name",
    "product-name",
    "value",
    "units",
    "series",
]


class EnergyDataValidator:
    def __init__(self):
        self.required_fields = REQUIRED_FIELDS

    def validate_records(self, records: list[dict]) -> dict:
        valid_records = []
        invalid_records = []
        business_keys = []

        for record in records:
            errors = self.validate_single_record(record)

            business_key = self.generate_business_key(record)

            if business_key:
                business_keys.append(business_key)

            if errors:
                invalid_records.append(
                    {
                        "record": record,
                        "errors": errors,
                    }
                )
            else:
                valid_records.append(record)

        duplicate_keys = self.find_duplicates(business_keys)

        summary = {
            "total_records": len(records),
            "valid_count": len(valid_records),
            "invalid_count": len(invalid_records),
            "duplicate_count": len(duplicate_keys),
            "duplicate_keys": duplicate_keys,
            "valid_records": valid_records,
            "invalid_records": invalid_records,
            "validated_at": datetime.now(timezone.utc).isoformat(),
        }

        logger.info(
            f"Validation completed | "
            f"Total: {summary['total_records']} | "
            f"Valid: {summary['valid_count']} | "
            f"Invalid: {summary['invalid_count']} | "
            f"Duplicates: {summary['duplicate_count']}"
        )

        return summary

    def validate_single_record(self, record: dict) -> list[str]:
        errors = []

        for field in self.required_fields:
            if field not in record or record[field] in [None, ""]:
                errors.append(f"Missing required field: {field}")

        value = record.get("value")

        try:
            numeric_value = float(value)

            if numeric_value < 0:
                errors.append("Negative price/value detected")

        except (TypeError, ValueError):
            errors.append("Invalid numeric value")

        period = record.get("period")

        if period:
            try:
                datetime.strptime(period, "%Y-%m-%d")
            except ValueError:
                errors.append("Invalid period date format")

        return errors

    def generate_business_key(self, record: dict):
        required_key_fields = [
            "period",
            "area-name",
            "product-name",
            "units",
            "series",
        ]

        if not all(record.get(field) for field in required_key_fields):
            return None

        return "|".join(str(record[field]) for field in required_key_fields)

    def find_duplicates(self, business_keys: list[str]) -> list[str]:
        counts = Counter(business_keys)

        return [
            key for key, count in counts.items()
            if count > 1
        ]


if __name__ == "__main__":
    sample_records = [
        {
            "period": "2026-05-18",
            "area-name": "U.S.",
            "product-name": "Diesel",
            "value": "5.596",
            "units": "$/GAL",
            "series": "sample_series",
        }
    ]

    validator = EnergyDataValidator()
    result = validator.validate_records(sample_records)

    print(result)
