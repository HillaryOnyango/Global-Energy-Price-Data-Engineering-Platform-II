from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from pymongo import MongoClient, UpdateOne
from pymongo.database import Database

from config.settings import settings
from app.utils.constants import DQ_COLLECTION, PIPELINE_RUNS_COLLECTION, PRODUCT_COLLECTIONS, RAW_COLLECTION

class MongoRepository:
    def __init__(self, uri: str | None = None, database: str | None = None) -> None:
        self.client = MongoClient(uri or settings.mongodb_uri)
        self.db: Database = self.client[database or settings.mongodb_database]

    def ensure_indexes(self) -> None:
        self.db[RAW_COLLECTION].create_index("ingestion_timestamp")
        self.db[PIPELINE_RUNS_COLLECTION].create_index("pipeline_run_id")
        self.db[DQ_COLLECTION].create_index("created_at")
        for collection in PRODUCT_COLLECTIONS.values():
            self.db[collection].create_index([
                ("country", 1), ("reporting_date", -1), ("product_type", 1)
            ])
            self.db[collection].create_index("batch_id")
            self.db[collection].create_index("business_key", unique=True)

    def insert_raw(self, raw_document: dict[str, Any]) -> str:
        result = self.db[RAW_COLLECTION].insert_one(raw_document)
        return str(result.inserted_id)

    def upsert_curated(self, records: list[dict[str, Any]]) -> dict[str, int]:
        counts = {"matched": 0, "modified": 0, "upserted": 0}
        by_collection: dict[str, list[UpdateOne]] = {}
        for record in records:
            collection = PRODUCT_COLLECTIONS.get(record.get("product_type"))
            if not collection:
                continue
            by_collection.setdefault(collection, []).append(
                UpdateOne({"business_key": record["business_key"]}, {"$set": record}, upsert=True)
            )

        for collection, operations in by_collection.items():
            if not operations:
                continue
            result = self.db[collection].bulk_write(operations, ordered=False)
            counts["matched"] += result.matched_count
            counts["modified"] += result.modified_count
            counts["upserted"] += len(result.upserted_ids)
        return counts

    def save_quality_result(self, result: dict[str, Any], batch_id: str | None = None) -> str:
        document = {**result, "batch_id": batch_id, "created_at": datetime.now(timezone.utc)}
        # Avoid storing all valid records in audit collection.
        document.pop("valid_records", None)
        return str(self.db[DQ_COLLECTION].insert_one(document).inserted_id)

    def save_pipeline_run(self, run: dict[str, Any]) -> str:
        run.setdefault("created_at", datetime.now(timezone.utc))
        return str(self.db[PIPELINE_RUNS_COLLECTION].insert_one(run).inserted_id)
