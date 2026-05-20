from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class Settings:
    energy_api_base_url: str = os.getenv("ENERGY_API_BASE_URL", "https://api.eia.gov/v2")
    energy_api_key: str = os.getenv("ENERGY_API_KEY", "")
    api_timeout_seconds: int = int(os.getenv("ENERGY_API_TIMEOUT_SECONDS", "30"))
    mongodb_uri: str = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
    mongodb_database: str = os.getenv("MONGODB_DATABASE", "global_energy_prices")
    source_name: str = os.getenv("SOURCE_NAME", "EIA_API")

settings = Settings()
