from datetime import datetime, timezone

from pymongo import UpdateOne

from app.database.mongo import db
from app.config.settings import settings
from app.utils.logger import get_logger

logger = get_logger(__name__)


class CuratedDataLoader:
    def __init__(self):
        self.collection_map = {
            "fuel": db[settings.FUEL_COLLECTION],
            "electricity": db[settings.ELECTRICITY_COLLECTION],
            "natural_gas": db[settings.NATURAL_GAS_COLLECTION],
            "unknown": db["unknown_energy_prices"],
        }

    def load_curated_records(self, records: list[dict]) -> dict:
        if not records:
            logger.warning("No curated records received for loading.")
            return {
                "inserted_or_updated_count": 0,
                "collection_summary": {},
            }

        collection_batches = self.group_records_by_collection(records)

        total_loaded = 0
        collection_summary = {}

        for product_type, grouped_records in collection_batches.items():
            collection = self.collection_map.get(
                product_type,
                db["unknown_energy_prices"],
            )

            operations = []

            for record in grouped_records:
                record["updated_at"] = datetime.now(timezone.utc).isoformat()

                filter_key = {
                    "country": record.get("country"),
                    "product_type": record.get("product_type"),
                    "reporting_date": record.get("reporting_date"),
                    "unit": record.get("unit"),
                    "source": record.get("source"),
                    "series": record.get("series"),
                }

                operations.append(
                    UpdateOne(
                        filter_key,
                        {"$set": record},
                        upsert=True,
                    )
                )

            if operations:
                result = collection.bulk_write(operations, ordered=False)

                loaded_count = result.upserted_count + result.modified_count

                total_loaded += loaded_count

                collection_summary[collection.name] = {
                    "matched_count": result.matched_count,
                    "modified_count": result.modified_count,
                    "upserted_count": result.upserted_count,
                    "loaded_count": loaded_count,
                }

                logger.info(
                    f"Loaded curated records into {collection.name} | "
                    f"Matched: {result.matched_count} | "
                    f"Modified: {result.modified_count} | "
                    f"Upserted: {result.upserted_count}"
                )

        return {
            "inserted_or_updated_count": total_loaded,
            "collection_summary": collection_summary,
        }

    def group_records_by_collection(self, records: list[dict]) -> dict:
        grouped = {}

        for record in records:
            product_type = record.get("product_type", "unknown")

            grouped.setdefault(product_type, []).append(record)

        return grouped

    def create_indexes(self):
        for product_type, collection in self.collection_map.items():
            collection.create_index(
                [
                    ("country", 1),
                    ("reporting_date", -1),
                    ("product_type", 1),
                    ("series", 1),
                ],
                name=f"{product_type}_business_lookup_idx",
            )

            collection.create_index(
                [("batch_id", 1)],
                name=f"{product_type}_batch_id_idx",
            )

        logger.info("Curated collection indexes created successfully.")


if __name__ == "__main__":
    sample_records = [
        {
            "country": "U.S.",
            "area_code": "NUS",
            "product_type": "fuel",
            "product_name": "No 2 Diesel Low Sulfur",
            "price": 5.596,
            "currency": "USD",
            "unit": "gal",
            "reporting_date": "2026-05-18",
            "source": "EIA",
            "series": "EMD_EPD2DXL0_PTE_NUS_DPG",
            "series_description": "U.S. Diesel Retail Prices",
            "batch_id": "batch_test_001",
            "ingestion_timestamp": datetime.now(timezone.utc).isoformat(),
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
    ]

    loader = CuratedDataLoader()
    loader.create_indexes()
    result = loader.load_curated_records(sample_records)

    print(result)
