from datetime import datetime, timezone

from app.utils.logger import get_logger

logger = get_logger(__name__)


class EnergyDataTransformer:
    def transform_records(
        self,
        records: list[dict],
        batch_id: str,
        source: str = "EIA",
    ) -> list[dict]:
        transformed_records = []

        for record in records:
            transformed_record = self.transform_single_record(
                record=record,
                batch_id=batch_id,
                source=source,
            )

            transformed_records.append(transformed_record)

        logger.info(
            f"Transformation completed | "
            f"Input records: {len(records)} | "
            f"Transformed records: {len(transformed_records)}"
        )

        return transformed_records

    def transform_single_record(
        self,
        record: dict,
        batch_id: str,
        source: str,
    ) -> dict:
        product_name = record.get("product-name", "")

        return {
            "country": record.get("area-name"),
            "area_code": record.get("duoarea"),
            "product_type": self.map_product_type(product_name),
            "product_name": product_name,
            "price": self.to_float(record.get("value")),
            "currency": self.extract_currency(record.get("units")),
            "unit": self.extract_unit(record.get("units")),
            "reporting_date": self.parse_date(record.get("period")),
            "source": source,
            "series": record.get("series"),
            "series_description": record.get("series-description"),
            "batch_id": batch_id,
            "ingestion_timestamp": datetime.now(timezone.utc).isoformat(),
            "created_at": datetime.now(timezone.utc).isoformat(),
        }

    def map_product_type(self, product_name: str) -> str:
        product_name_lower = product_name.lower()

        if "diesel" in product_name_lower:
            return "fuel"

        if "gasoline" in product_name_lower:
            return "fuel"

        if "electric" in product_name_lower:
            return "electricity"

        if "natural gas" in product_name_lower:
            return "natural_gas"

        return "unknown"

    def to_float(self, value):
        try:
            return float(value)
        except (TypeError, ValueError):
            return None

    def extract_currency(self, units: str) -> str:
        if not units:
            return "unknown"

        if "$" in units:
            return "USD"

        return "unknown"

    def extract_unit(self, units: str) -> str:
        if not units:
            return "unknown"

        if "/" in units:
            return units.split("/")[-1].lower()

        return units.lower()

    def parse_date(self, value: str):
        if not value:
            return None

        try:
            return datetime.strptime(value, "%Y-%m-%d").date().isoformat()
        except ValueError:
            return None


if __name__ == "__main__":
    sample_records = [
        {
            "period": "2026-05-18",
            "duoarea": "NUS",
            "area-name": "U.S.",
            "product-name": "No 2 Diesel Low Sulfur",
            "value": "5.596",
            "units": "$/GAL",
            "series": "EMD_EPD2DXL0_PTE_NUS_DPG",
            "series-description": "U.S. Diesel Retail Prices",
        }
    ]

    transformer = EnergyDataTransformer()

    transformed = transformer.transform_records(
        records=sample_records,
        batch_id="batch_test_001",
    )

    print(transformed)
