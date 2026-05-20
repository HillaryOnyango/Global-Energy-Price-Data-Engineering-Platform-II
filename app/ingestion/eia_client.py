from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

import requests

from config.settings import settings
from app.utils.logger import get_logger

logger = get_logger(__name__)

class EIAClient:
    """Small API client for EIA-style JSON endpoints.

    Adjust `fetch_prices` endpoint/params after choosing the exact EIA route.
    The rest of the pipeline expects a list of normalized-ish dictionaries.
    """

    def __init__(self, base_url: str | None = None, api_key: str | None = None) -> None:
        self.base_url = (base_url or settings.energy_api_base_url).rstrip("/")
        self.api_key = api_key if api_key is not None else settings.energy_api_key

    def fetch_prices(self, product_type: str, frequency: str = "daily") -> dict[str, Any]:
        batch_id = str(uuid4())
        endpoint = f"{self.base_url}/energy-prices/{product_type}"
        params = {"api_key": self.api_key, "frequency": frequency}
        logger.info("Fetching %s prices from %s", product_type, endpoint)

        response = requests.get(endpoint, params=params, timeout=settings.api_timeout_seconds)
        response.raise_for_status()
        payload = response.json()
        return {
            "batch_id": batch_id,
            "source": settings.source_name,
            "product_type": product_type,
            "ingestion_timestamp": datetime.now(timezone.utc).isoformat(),
            "payload": payload,
        }
