from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

from app.loaders.mongo import MongoRepository
from app.utils.constants import DQ_COLLECTION, PIPELINE_RUNS_COLLECTION, PRODUCT_COLLECTIONS

class ReportingService:
    def __init__(self, repo: MongoRepository | None = None) -> None:
        self.repo = repo or MongoRepository()
        self.db = self.repo.db

    def latest_prices(self, limit: int = 100) -> list[dict[str, Any]]:
        rows: list[dict[str, Any]] = []
        for collection in PRODUCT_COLLECTIONS.values():
            cursor = self.db[collection].find({}, {"_id": 0, "raw_record": 0}).sort("reporting_date", -1).limit(limit)
            rows.extend(list(cursor))
        return rows[:limit]

    def twenty_four_hour_summary(self) -> dict[str, Any]:
        since = datetime.now(timezone.utc) - timedelta(hours=24)
        summary: dict[str, Any] = {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "products": {},
            "latest_pipeline_run": self.db[PIPELINE_RUNS_COLLECTION].find_one({}, {"_id": 0}, sort=[("created_at", -1)]),
            "latest_quality_result": self.db[DQ_COLLECTION].find_one({}, {"_id": 0}, sort=[("created_at", -1)]),
        }

        for product_type, collection in PRODUCT_COLLECTIONS.items():
            records = list(self.db[collection].find({"reporting_date": {"$gte": since}}, {"_id": 0, "raw_record": 0}))
            summary["products"][product_type] = {
                "records_last_24h": len(records),
                "max_price": max((r.get("price", 0) for r in records), default=None),
                "min_price": min((r.get("price", 0) for r in records), default=None),
            }
        return summary
