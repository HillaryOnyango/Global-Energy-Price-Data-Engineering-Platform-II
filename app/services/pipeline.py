from __future__ import annotations

from datetime import datetime, timezone

from app.ingestion.eia_client import EIAClient
from app.ingestion.parser import parse_eia_payload
from app.loaders.mongo import MongoRepository
from app.transformation.normalizer import normalize_records
from app.validation.quality_checks import validate_records


def run_pipeline(product_types: list[str] | None = None) -> dict:
    product_types = product_types or ["fuel", "electricity", "natural_gas"]
    client = EIAClient()
    repo = MongoRepository()
    repo.ensure_indexes()

    final = {"started_at": datetime.now(timezone.utc).isoformat(), "products": {}}
    for product_type in product_types:
        raw = client.fetch_prices(product_type=product_type)
        repo.insert_raw(raw)
        parsed = parse_eia_payload(raw)
        normalized = normalize_records(parsed)
        validation = validate_records(normalized)
        repo.save_quality_result(validation.to_dict(), batch_id=raw.get("batch_id"))
        load_result = repo.upsert_curated(validation.valid_records)
        final["products"][product_type] = {
            "batch_id": raw.get("batch_id"),
            "validation": validation.to_dict() | {"valid_records": "omitted"},
            "load_result": load_result,
        }
    final["finished_at"] = datetime.now(timezone.utc).isoformat()
    repo.save_pipeline_run({"pipeline_run_id": final["started_at"], "status": "success", "result": final})
    return final
