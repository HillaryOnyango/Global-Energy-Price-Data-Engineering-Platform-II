RAW_COLLECTION = "raw_api_data"
PIPELINE_RUNS_COLLECTION = "pipeline_runs"
DQ_COLLECTION = "data_quality_checks"

PRODUCT_COLLECTIONS = {
    "fuel": "fuel_prices",
    "electricity": "electricity_prices",
    "natural_gas": "natural_gas_prices",
}

REQUIRED_FIELDS = [
    "country",
    "product_type",
    "price",
    "currency",
    "unit",
    "reporting_date",
    "source",
]
