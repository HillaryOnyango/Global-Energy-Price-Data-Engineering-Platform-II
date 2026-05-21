from datetime import datetime, timezone

from app.database.mongo import db
from app.utils.logger import get_logger

logger = get_logger(__name__)


class RawDataLoader:
    def __init__(self):
        self.collection = db["raw_api_data"]

    def load_raw_data(self, ingestion_result: dict):
        """
        Store raw API payload into MongoDB.
        """

        if not ingestion_result:
            logger.error("No ingestion result received.")

            return None

        document = {
            "batch_id": ingestion_result["batch_id"],
            "source": ingestion_result["source"],
            "ingestion_timestamp": ingestion_result[
                "ingestion_timestamp"
            ],
            "loaded_at": datetime.now(
                timezone.utc
            ).isoformat(),
            "raw_data": ingestion_result["raw_data"],
        }

        try:
            result = self.collection.insert_one(document)

            logger.info(
                f"Raw data inserted successfully | "
                f"Document ID: {result.inserted_id}"
            )

            return str(result.inserted_id)

        except Exception as error:
            logger.error(
                f"Failed to insert raw data into MongoDB: {error}"
            )

            return None
