from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "Global Energy Price Platform"
    APP_ENV: str = "development"
    DEBUG: bool = True

    EIA_API_KEY: str
    EIA_BASE_URL: str = "https://api.eia.gov/v2"

    MONGO_URI: str = "mongodb://localhost:27017"
    MONGO_DB_NAME: str = "global_energy_prices"

    RAW_COLLECTION: str = "raw_api_data"
    FUEL_COLLECTION: str = "fuel_prices"
    ELECTRICITY_COLLECTION: str = "electricity_prices"
    NATURAL_GAS_COLLECTION: str = "natural_gas_prices"

    PIPELINE_RUNS_COLLECTION: str = "pipeline_runs"
    DATA_QUALITY_COLLECTION: str = "data_quality_checks"

    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()
