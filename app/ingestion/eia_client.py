import requests
from datetime import datetime, timezone

from app.config.settings import settings
from app.utils.logger import get_logger

logger = get_logger(__name__)


class EIAClient:
    def __init__(self):
        self.base_url = settings.EIA_BASE_URL
        self.api_key = settings.EIA_API_KEY

    def fetch_energy_data(self, endpoint: str, params: dict = None):
        """
        Fetch data from the EIA API.
        """

        if params is None:
            params = {}

        params["api_key"] = self.api_key

        url = f"{self.base_url}/{endpoint}"

        logger.info(f"Sending request to EIA API: {url}")

        try:
            response = requests.get(url, params=params, timeout=30)

            response.raise_for_status()

            logger.info(
                f"Successful API request | Status Code: {response.status_code}"
            )

            return {
                "success": True,
                "status_code": response.status_code,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "data": response.json(),
            }

        except requests.exceptions.HTTPError as http_error:
            logger.error(f"HTTP Error: {http_error}")

        except requests.exceptions.ConnectionError as connection_error:
            logger.error(f"Connection Error: {connection_error}")

        except requests.exceptions.Timeout as timeout_error:
            logger.error(f"Timeout Error: {timeout_error}")

        except requests.exceptions.RequestException as request_error:
            logger.error(f"Request Exception: {request_error}")

        return {
            "success": False,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "data": None,
        }
