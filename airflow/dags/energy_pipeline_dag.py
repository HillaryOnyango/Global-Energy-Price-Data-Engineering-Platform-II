from __future__ import annotations

from datetime import timedelta

from airflow.decorators import dag, task
from pendulum import datetime

@dag(
    dag_id="global_energy_price_pipeline",
    start_date=datetime(2026, 1, 1, tz="UTC"),
    schedule="@daily",
    catchup=False,
    default_args={"retries": 2, "retry_delay": timedelta(minutes=5)},
    tags=["energy", "mongodb", "data-engineering"],
)
def energy_pipeline_dag():
    @task
    def ingest_validate_transform_load():
        from app.services.pipeline import run_pipeline
        return run_pipeline()

    @task
    def generate_report():
        from app.services.reporting import ReportingService
        return ReportingService().twenty_four_hour_summary()

    ingest_validate_transform_load() >> generate_report()

energy_pipeline_dag()
