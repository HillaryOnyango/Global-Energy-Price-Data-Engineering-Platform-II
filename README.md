# Global Energy Price Data Engineering Platform II
**Real-Time Energy Market Intelligence Pipeline**

An end-to-end modern data engineering platform that ingests, validates, transforms, orchestrates, and visualizes global energy market data using Python, MongoDB, Apache Airflow 3, Flask, Docker, UV, and Chart.js.

The platform simulates a production-grade analytics backend for an energy intelligence company that tracks fuel, electricity, and natural gas prices in near real time.

---

## Project Overview

This platform demonstrates modern data engineering concepts including:

- External API ingestion
- ETL / ELT pipeline design
- Workflow orchestration
- Schema validation
- Data quality monitoring
- Raw vs curated data modeling
- Observability & metadata tracking
- Flask API engineering
- Interactive dashboards
- Containerization with Docker
- Modular Python architecture
- Production-style logging
- Integration-ready infrastructure

The system continuously collects energy pricing datasets from the U.S. Energy Information Administration (EIA), validates and transforms the records, stores both raw and analytics-ready datasets in MongoDB, orchestrates workflows with Apache Airflow, and exposes analytics through a Flask dashboard and APIs.

---

## Business Problem

Energy prices directly impact:

- Inflation trends
- Transportation costs
- Household cost of living
- Manufacturing expenses
- Logistics and supply chains
- Government policy planning

Organizations need reliable answers to questions like:

- Which regions experienced the highest fuel price increase today?
- Which states have abnormal electricity price spikes?
- Are there stale or duplicate records in the latest ingestion batch?
- How many records failed validation?
- What was the latest successful pipeline execution?
- Which regions currently have the highest natural gas costs?

Without a centralized data platform, organizations rely on inconsistent spreadsheets and manual reporting pipelines.

This project solves that by building a scalable, observable, and production-style data platform.

---

## High-Level Architecture

```
                    ┌────────────────────┐
                    │     EIA API        │
                    │ External Data Src  │
                    └─────────┬──────────┘
                              │
                              ▼
                    ┌────────────────────┐
                    │ Ingestion Layer    │
                    │ API Client         │
                    │ Metadata Capture   │
                    └─────────┬──────────┘
                              │
                              ▼
                    ┌────────────────────┐
                    │ Raw Data Zone      │
                    │ MongoDB Raw Store  │
                    └─────────┬──────────┘
                              │
                              ▼
                    ┌────────────────────┐
                    │ Validation Layer   │
                    │ Quality Checks     │
                    └─────────┬──────────┘
                              │
                              ▼
                    ┌────────────────────┐
                    │ Transformation     │
                    │ Standardization    │
                    └─────────┬──────────┘
                              │
                              ▼
                    ┌────────────────────┐
                    │ Curated Data Zone  │
                    │ Analytics Ready    │
                    └─────────┬──────────┘
                              │
                              ▼
                    ┌────────────────────┐
                    │ Apache Airflow 3   │
                    │ Orchestration      │
                    └─────────┬──────────┘
                              │
                              ▼
                    ┌────────────────────┐
                    │ Flask Dashboard    │
                    │ Visualization API  │
                    └────────────────────┘
```

---

## Features

- Multi-source energy ingestion
- ETL / ELT pipeline design
- MongoDB raw + curated zones
- Data validation & quality monitoring
- Apache Airflow orchestration
- Flask analytics dashboard
- Chart.js visualizations
- Docker containerization
- Metadata tracking
- Production-style architecture

---

## Technology Stack

| Layer | Technology |
|---|---|
| Language | Python 3.12 |
| Database | MongoDB |
| Workflow Orchestration | Apache Airflow 3 |
| Backend API | Flask |
| Visualization | Chart.js |
| Containerization | Docker |
| Package Manager | UV |
| Data Source | EIA API |

---

## Project Structure

```
Global-Energy-Price-Platform/
│
├── airflow/
│   └── dags/
│
├── app/
│   ├── config/
│   ├── database/
│   ├── ingestion/
│   ├── loaders/
│   ├── transformation/
│   ├── validation/
│   ├── utils/
│   └── pipeline.py
│
├── flask_app/
│   ├── routes/
│   ├── static/
│   └── templates/
│
├── tests/
│
├── docker-compose.yml
├── Dockerfile
├── pyproject.toml
├── uv.lock
└── README.md
```

---

## Clone Repository

```bash
git clone https://github.com/HillaryOnyango/Global-Energy-Price-Data-Engineering-Platform-II.git

cd Global-Energy-Price-Data-Engineering-Platform-II
```

## Install UV

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Verify Installation

```bash
uv --version
```

## Create Virtual Environment

```bash
uv venv
```

## Activate Environment

```bash
source .venv/bin/activate
```

## Install Dependencies

```bash
uv sync
```

---

## Configure Environment Variables

Create `.env`:

```env
APP_NAME=Global Energy Price Platform
APP_ENV=development
DEBUG=True

EIA_API_KEY=your_eia_api_key

MONGO_URI=mongodb://localhost:27017
MONGO_DB_NAME=global_energy_prices

LOG_LEVEL=INFO
```

### Get EIA API Key

Register for a free EIA API key: [EIA Open Data API Registration](https://www.eia.gov/opendata/)

---

## Run MongoDB Using Docker

### Pull MongoDB Image

```bash
docker pull mongo
```

### Run MongoDB Container

```bash
docker run -d \
  --name global-energy-mongodb \
  -p 27017:27017 \
  mongo
```

### Verify Container

```bash
docker ps
```

---

## Run ETL Pipeline

```bash
uv run python -m app.pipeline
```

Expected output:

```
PIPELINE EXECUTION SUCCESSFUL
```

---

## Run Flask Dashboard

```bash
PYTHONPATH=. uv run python -m flask --app flask_app.app run
```

Open in browser: [http://127.0.0.1:5000](http://127.0.0.1:5000)

### Dashboard Includes

- Fuel price visualization
- Natural gas visualization
- Electricity visualization
- Pipeline monitoring
- Data quality metrics
- Regional analytics
- Interactive charts

---

## Query MongoDB

Access MongoDB shell:

```bash
docker exec -it global-energy-mongodb mongosh
```

Switch database:

```js
use global_energy_prices
```

View collections:

```js
show collections
```

Example queries:

```js
db.fuel_prices.find().pretty()

db.natural_gas_prices.find().pretty()

db.electricity_prices.find().pretty()

db.pipeline_runs.find().pretty()

db.data_quality_checks.find().pretty()
```

---

## Airflow Scheduling

The Airflow DAG schedules the ETL pipeline every 24 hours.

DAG location:

```
airflow/dags/energy_pipeline_dag.py
```

---

## Dockerization Benefits

This project uses Docker for:

- Consistent environments
- Easier deployment
- Service isolation
- Reproducibility
- Production-style infrastructure

---

## Example Analytics Questions

The platform can answer questions like:

- Which region has the highest diesel prices?
- Which state has the cheapest electricity?
- Which natural gas markets are most volatile?
- Which records failed validation?
- How many records were processed today?
- When was the latest successful pipeline execution?

---

## Future Improvements

Potential future enhancements:

- Kafka streaming ingestion
- Redis caching
- PostgreSQL analytics warehouse
- Kubernetes deployment
- CI/CD pipelines
- Prometheus monitoring
- Grafana dashboards
- Machine learning forecasting
- Historical trend analysis
- Global non-U.S. datasets
- Authentication & RBAC

---

## Author

**Hillary Onyango**

GitHub Repository: [Global Energy Price Data Engineering Platform II](https://github.com/HillaryOnyango/Global-Energy-Price-Data-Engineering-Platform-II)
