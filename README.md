Global Energy Price Data Engineering Platform II
Real-Time Energy Market Intelligence Pipeline
An end-to-end modern data engineering platform that ingests, validates, transforms, orchestrates, and visualizes global energy market data using Python, MongoDB, Apache Airflow 3, Flask, Docker, UV, and Chart.js.

Features
·	Multi-source energy ingestion
·	ETL / ELT pipeline design
·	MongoDB raw + curated zones
·	Data validation & quality monitoring
·	Apache Airflow orchestration
·	Flask analytics dashboard
·	Chart.js visualizations
·	Docker containerization
·	Metadata tracking
·	Production-style architecture

Clone Repository
git clone https://github.com/HillaryOnyango/Global-Energy-Price-Data-Engineering-Platform-II.git

cd Global-Energy-Price-Data-Engineering-Platform-II


Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh

Verify installation:
uv --version


Create Virtual Environment
uv venv

Activate:
source .venv/bin/activate


Install Dependencies
uv sync


Configure Environment Variables
Create .env
APP_NAME=Global Energy Price Platform
APP_ENV=development
DEBUG=True

EIA_API_KEY=your_eia_api_key

MONGO_URI=mongodb://localhost:27017
MONGO_DB_NAME=global_energy_prices

LOG_LEVEL=INFO


Run MongoDB Using Docker
docker pull mongo

docker run -d   --name global-energy-mongodb   -p 27017:27017   mongo

Verify:
docker ps


Run ETL Pipeline
uv run python -m app.pipeline


Run Flask Dashboard
PYTHONPATH=. uv run python -m flask --app flask_app.app run

Open:
http://127.0.0.1:5000


Query MongoDB
docker exec -it global-energy-mongodb mongosh

use global_energy_prices

show collections


Dashboard Includes
·	Fuel price visualization
·	Natural gas visualization
·	Electricity visualization
·	Pipeline monitoring
·	Data quality metrics
·	Regional analytics

Technology Stack
Layer	Technology
Language	Python 3.12
Database	MongoDB
Workflow	Apache Airflow 3
Backend	Flask
Visualization	Chart.js
Containerization	Docker
Package Manager	UV


Author
Hillary Onyango
