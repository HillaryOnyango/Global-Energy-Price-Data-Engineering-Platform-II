# Global Energy Price Data Engineering Platform II

## Real-Time Energy Market Intelligence Pipeline

An end-to-end modern data engineering platform that ingests, validates, transforms, orchestrates, and serves global energy market data using Python, MongoDB, Apache Airflow 3, and Flask.

This project simulates a production-grade analytics backend for an energy intelligence company that tracks global fuel, electricity, and natural gas prices in near real time.

---

# Project Overview

The platform is designed to solve real-world data engineering challenges around:

- external API ingestion
- scalable ETL/ELT workflows
- schema validation
- raw vs curated data modeling
- orchestration and observability
- metadata tracking
- analytics delivery
- operational reliability

The system continuously collects energy pricing datasets from the EIA API, processes and validates records, stores both raw and analytics-ready datasets in MongoDB, orchestrates workflows using Apache Airflow, and exposes reporting through Flask APIs and dashboards.

---

# Business Problem

Energy prices directly impact:

- inflation trends
- transportation costs
- household cost of living
- manufacturing expenses
- logistics and supply chains
- government policy planning

Organizations need reliable answers to questions like:

- Which countries experienced the highest fuel price increase today?
- Which regions have abnormal electricity price spikes?
- Are there stale or duplicate records in the latest ingestion batch?
- How many records failed quality validation?
- What was the latest successful pipeline execution?

Without a centralized data platform, organizations rely on inconsistent spreadsheets and manual reporting pipelines.

This project solves that by building a reliable, observable, and scalable modern data platform.

---

# High-Level Architecture

```text
                    ┌────────────────────┐
                    │    EIA API         │
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
                    │ Flask API          │
                    │ Dashboard          │
                    └────────────────────┘
