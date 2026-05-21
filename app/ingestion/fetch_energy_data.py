from uuid import uuid4
from datetime import datetime, timezone
from app.loaders.raw_loader import RawDataLoader
from app.ingestion.eia_client import EIAClient
from app.utils.logger import get_logger
from app.loaders.raw_loader import RawDataLoader

logger = get_logger(__name__)


def generate_batch_id():
    return f"batch_{uuid4().hex[:10]}"


def fetch_energy_prices():
    logger.info("Starting energy data ingestion process.")

    client = EIAClient()

    batch_id = generate_batch_id()

    ingestion_timestamp = datetime.now(timezone.utc).isoformat()

    endpoint = "petroleum/pri/gnd/data"

    params = {
        "frequency": "weekly",
        "data[0]": "value",
        "sort[0][column]": "period",
        "sort[0][direction]": "desc",
        "offset": 0,
        "length": 10,
    }

    response = client.fetch_energy_data(
        endpoint=endpoint,
        params=params,
    )

    if response["success"]:
        logger.info("Energy data fetched successfully.")

        result = {
            "batch_id": batch_id,
            "ingestion_timestamp": ingestion_timestamp,
            "source": "EIA",
            "raw_data": response["data"],
        }

        loader = RawDataLoader()

        document_id = loader.load_raw_data(result)

        logger.info(f"Batch ID: {batch_id}")

        logger.info(f"MongoDB Document ID: {document_id}")

        return result

    logger.error("Energy data ingestion failed.")

    return None


if __name__ == "__main__":
    data = fetch_energy_prices()

    if data:
        print(data)
