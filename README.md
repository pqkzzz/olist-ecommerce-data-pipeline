# Olist E-commerce Data Pipeline

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white" />
  <img src="https://img.shields.io/badge/dbt-FF694B?style=for-the-badge&logo=dbt&logoColor=white" />
  <img src="https://img.shields.io/badge/Apache%20Airflow-017CEE?style=for-the-badge&logo=apacheairflow&logoColor=white" />
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" />
  <img src="https://img.shields.io/badge/Metabase-509EE3?style=for-the-badge&logo=metabase&logoColor=white" />
</p>

<p align="center">
  <b>End-to-end batch ELT pipeline using Python, PostgreSQL, dbt, Airflow, Docker and Metabase.</b>
</p>

<p align="center">
  <a href="#1-overview">Overview</a> •
  <a href="#4-project-architecture">Architecture</a> •
  <a href="#5-data-pipeline-flow">Pipeline</a> •
  <a href="#6-data-model">Data Model</a> •
  <a href="#8-airflow-orchestration">Airflow</a> •
  <a href="#12-how-to-run-the-project">How to Run</a>
</p>

---

## 1. Overview

This project is an end-to-end **batch ELT data pipeline** built with the Olist Brazilian E-commerce public dataset.

The pipeline loads raw CSV files into PostgreSQL, transforms the data with dbt, models analytical fact and dimension tables, validates data quality, visualizes business metrics in Metabase, and orchestrates the whole workflow with Airflow.

The main goal of this project is to simulate a real-world Data Engineering workflow:

```text
Raw CSV Data
→ PostgreSQL Raw Layer
→ dbt Staging Layer
→ dbt Warehouse Layer
→ Data Quality Checks
→ Metabase Dashboard
→ Airflow Orchestration
```

---

## 2. Tech Stack

| Tool | Purpose |
|---|---|
| Python | Load raw CSV data into PostgreSQL and run custom data quality checks |
| PostgreSQL | Store raw, staging, and warehouse data |
| dbt | Transform raw data into staging views and warehouse fact/dimension tables |
| Airflow | Orchestrate the pipeline tasks |
| Metabase | Build business dashboard and visualize insights |
| Docker Compose | Run PostgreSQL, Metabase, and Airflow services locally |
| SQL | Data transformation, modeling, and analytics queries |

---

## 3. Dataset

This project uses the **Olist Brazilian E-commerce Public Dataset**.

The dataset contains real e-commerce data such as orders, order items, customers, products, sellers, payments, and reviews.

Expected raw CSV files:

```text
data/raw/
├── olist_customers_dataset.csv
├── olist_geolocation_dataset.csv
├── olist_order_items_dataset.csv
├── olist_order_payments_dataset.csv
├── olist_order_reviews_dataset.csv
├── olist_orders_dataset.csv
├── olist_products_dataset.csv
├── olist_sellers_dataset.csv
└── product_category_name_translation.csv
```

> Note: Raw CSV files are not required to be committed to GitHub. Download the dataset and place all CSV files inside `data/raw/`.

---

## 4. Project Architecture

```text
                  ┌──────────────────────┐
                  │   Olist CSV Files     │
                  └──────────┬───────────┘
                             │
                             ▼
                  ┌──────────────────────┐
                  │ Python Load Script    │
                  │ scripts/load_raw_data │
                  └──────────┬───────────┘
                             │
                             ▼
                  ┌──────────────────────┐
                  │ PostgreSQL            │
                  │ raw schema            │
                  └──────────┬───────────┘
                             │
                             ▼
                  ┌──────────────────────┐
                  │ dbt Staging Models    │
                  │ staging schema         │
                  └──────────┬───────────┘
                             │
                             ▼
                  ┌──────────────────────┐
                  │ dbt Warehouse Models  │
                  │ warehouse schema       │
                  └──────────┬───────────┘
                             │
              ┌──────────────┴──────────────┐
              ▼                             ▼
   ┌──────────────────────┐      ┌──────────────────────┐
   │ Data Quality Checks   │      │ Metabase Dashboard    │
   │ dbt + Python          │      │ Business Analytics    │
   └──────────────────────┘      └──────────────────────┘
                             ▲
                             │
                  ┌──────────────────────┐
                  │ Airflow DAG           │
                  │ Pipeline Orchestration│
                  └──────────────────────┘
```

---

## 5. Data Pipeline Flow

The project follows a layered data architecture:

```text
raw → staging → warehouse
```

### 5.1 Raw Layer

The `raw` schema stores data loaded directly from CSV files.

Example raw tables:

```text
raw.customers
raw.orders
raw.order_items
raw.products
raw.sellers
raw.order_payments
raw.order_reviews
raw.product_category_translation
raw.geolocation
```

The raw layer is used to preserve the original source data for traceability and debugging.

---

### 5.2 Staging Layer

The `staging` schema contains cleaned and standardized views created by dbt.

Example staging models:

```text
staging.stg_orders
staging.stg_order_items
staging.stg_customers
staging.stg_products
staging.stg_sellers
staging.stg_payments
staging.stg_reviews
```

The staging layer is responsible for:

- Selecting useful columns
- Casting data types
- Standardizing text values
- Translating product category names
- Preparing data for warehouse modeling

In this project, staging models are materialized as **views** because they are lightweight transformations and do not need to store duplicated data.

---

### 5.3 Warehouse Layer

The `warehouse` schema contains analytical fact and dimension tables.

Dimension tables:

```text
warehouse.dim_customers
warehouse.dim_products
warehouse.dim_sellers
warehouse.dim_dates
```

Fact tables:

```text
warehouse.fact_order_items
warehouse.fact_payments
warehouse.fact_reviews
```

The warehouse layer is used by Metabase for business reporting and dashboarding.

Warehouse models are materialized as **tables** because they contain final analytical data with joins, metrics, and business logic. This improves dashboard query performance and provides a stable reporting layer.

---

## 6. Data Model

The main analytical model follows a star schema design.

```text
                 dim_customers
                       |
dim_products ─── fact_order_items ─── dim_sellers
                       |
                   dim_dates
```

### Main Fact Table: `fact_order_items`

The grain of `fact_order_items` is:

```text
1 row = 1 product item in 1 order
```

This grain is chosen because one order can contain multiple products. Modeling at the order-item level allows analysis by product, category, seller, customer location, and time.

Important columns:

| Column | Description |
|---|---|
| order_id | Order identifier |
| order_item_id | Item sequence inside an order |
| customer_id | Customer identifier |
| product_id | Product identifier |
| seller_id | Seller identifier |
| order_date_id | Date key for joining with `dim_dates` |
| order_status | Status of the order |
| price | Product item price |
| freight_value | Shipping cost |
| total_order_item_value | `price + freight_value` |
| is_late_delivery | Flag indicating whether the order was delivered late |
| delivery_days | Number of days from purchase to delivery |

---

## 7. Data Quality

This project includes two layers of data validation:

```text
dbt tests + Python data quality checks
```

### 7.1 dbt Tests

dbt tests are defined in:

```text
dbt_project/olist_dbt/models/schema.yml
```

They validate basic model and column-level rules such as:

- Primary keys should not be null
- Dimension keys should be unique
- Important fact columns should not be null

Examples:

```text
not_null
unique
```

### 7.2 Python Data Quality Checks

Custom data quality checks are defined in:

```text
scripts/data_quality.py
```

The script validates rules such as:

- Raw order tables are not empty
- Order IDs are not null
- Order item prices are not negative
- Freight values are not negative
- Payment values are not negative
- Order statuses are valid
- Warehouse fact table has data

If any check fails, the script raises an exception. In Airflow, this causes the pipeline task to fail.

---

## 8. Airflow Orchestration

Airflow is used to orchestrate the pipeline.

The DAG file is located at:

```text
dags/olist_pipeline_dag.py
```

Current pipeline flow:

```text
check_project_files
→ load_raw_data
→ dbt_run
→ dbt_test
→ data_quality_check
```

### Task Details

| Task | Purpose |
|---|---|
| check_project_files | Verify that Airflow can access the mounted project files |
| load_raw_data | Run Python script to load CSV files into PostgreSQL raw schema |
| dbt_run | Build dbt staging views and warehouse tables |
| dbt_test | Run dbt tests defined in `schema.yml` |
| data_quality_check | Run custom Python data quality checks |

The DAG can be triggered manually from the Airflow UI. It can also be scheduled by changing the `schedule` argument in the DAG file.

Example daily schedule:

```python
schedule="0 2 * * *"
```

This would run the pipeline every day at 2:00 AM.

---

## 9. Dashboard

Metabase is used to build the analytics dashboard from the warehouse tables.

The dashboard answers business questions such as:

- What is the total revenue?
- What is the monthly revenue trend?
- Which product categories generate the most revenue?
- Which customer states generate the most revenue?
- What is the order status distribution?
- What is the late delivery rate?
- Which product categories have the highest review scores?

Recommended dashboard screenshot path:

```text
screenshots/dashboard.png
```

Example README image reference:

```md
![Metabase Dashboard](screenshots/dashboard.png)
```

---

## 10. Project Structure

```text
olist-ecommerce-data-pipeline/
│
├── dags/
│   └── olist_pipeline_dag.py
│
├── data/
│   └── raw/
│       └── <Olist CSV files>
│
├── dbt_project/
│   └── olist_dbt/
│       ├── macros/
│       │   └── generate_schema_name.sql
│       │
│       ├── models/
│       │   ├── staging/
│       │   │   ├── stg_orders.sql
│       │   │   ├── stg_order_items.sql
│       │   │   ├── stg_customers.sql
│       │   │   ├── stg_products.sql
│       │   │   ├── stg_sellers.sql
│       │   │   ├── stg_payments.sql
│       │   │   └── stg_reviews.sql
│       │   │
│       │   ├── marts/
│       │   │   ├── dim_customers.sql
│       │   │   ├── dim_products.sql
│       │   │   ├── dim_sellers.sql
│       │   │   ├── dim_dates.sql
│       │   │   ├── fact_order_items.sql
│       │   │   ├── fact_payments.sql
│       │   │   └── fact_reviews.sql
│       │   │
│       │   └── schema.yml
│       │
│       ├── dbt_project.yml
│       ├── profiles.yml.example
│       └── profiles.yml
│
├── logs/
│
├── plugins/
│
├── scripts/
│   ├── load_raw_data.py
│   └── data_quality.py
│
├── screenshots/
│   ├── dashboard.png
│   └── airflow_dag_success.png
│
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## 11. Environment Variables

Create a `.env` file in the project root.

For local Python/dbt execution from Windows:

```env
DB_HOST=localhost
DB_USER=admin
DB_PASSWORD=admin
DB_PORT=5433
DB_NAME=olist_dw
DB_URL=postgresql://admin:admin@localhost:5433/olist_dw
```

For Docker services such as Airflow and Metabase, containers connect to PostgreSQL internally using:

```text
postgres:5432
```

Important distinction:

| Environment | Host | Port |
|---|---|---|
| Local Windows Python/dbt | localhost | 5433 |
| Docker containers | postgres | 5432 |

---

## 12. How to Run the Project

### 12.1 Start Docker Services

```bash
docker compose up -d
```

This starts PostgreSQL, Metabase, Airflow metadata database, Airflow webserver, and Airflow scheduler.

Check running containers:

```bash
docker compose ps
```

---

### 12.2 Create Python Virtual Environment

```bash
python -m venv venv
```

Activate on Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

### 12.3 Load Raw Data Manually

```bash
python scripts/load_raw_data.py
```

This loads all CSV files from `data/raw/` into the PostgreSQL `raw` schema.

---

### 12.4 Run dbt Manually

Move into the dbt project directory:

```bash
cd dbt_project/olist_dbt
```

Check dbt connection:

```bash
dbt debug --profiles-dir .
```

Run dbt models:

```bash
dbt run --profiles-dir .
```

Run dbt tests:

```bash
dbt test --profiles-dir .
```

Return to the project root:

```bash
cd ../..
```

---

### 12.5 Run Python Data Quality Checks Manually

```bash
python scripts/data_quality.py
```

---

### 12.6 Run the Full Pipeline with Airflow

Open Airflow UI:

```text
http://localhost:8081
```

Default login:

```text
Username: admin
Password: admin
```

Trigger the DAG:

```text
olist_ecommerce_data_pipeline
```

Expected task flow:

```text
check_project_files
→ load_raw_data
→ dbt_run
→ dbt_test
→ data_quality_check
```

All tasks should finish with `success`.

---

### 12.7 Open Metabase Dashboard

Open Metabase UI:

```text
http://localhost:3000
```

Use the following PostgreSQL connection settings inside Metabase:

```text
Host: postgres
Port: 5432
Database name: olist_dw
Username: admin
Password: admin
```

Metabase should query data from the `warehouse` schema, not directly from the `raw` schema.

---

## 13. Example Analytics Queries

### Monthly Revenue Trend

```sql
SELECT
    DATE_TRUNC('month', order_purchase_timestamp) AS month,
    SUM(price) AS revenue
FROM warehouse.fact_order_items
WHERE order_status = 'delivered'
GROUP BY month
ORDER BY month;
```

### Top 10 Categories by Revenue

```sql
SELECT
    p.product_category_name,
    SUM(f.price) AS revenue
FROM warehouse.fact_order_items f
LEFT JOIN warehouse.dim_products p
    ON f.product_id = p.product_id
WHERE f.order_status = 'delivered'
GROUP BY p.product_category_name
ORDER BY revenue DESC
LIMIT 10;
```

### Revenue by Customer State

```sql
SELECT
    c.customer_state,
    SUM(f.price) AS revenue
FROM warehouse.fact_order_items f
LEFT JOIN warehouse.dim_customers c
    ON f.customer_id = c.customer_id
WHERE f.order_status = 'delivered'
GROUP BY c.customer_state
ORDER BY revenue DESC;
```

### Late Delivery Rate

```sql
SELECT
    CASE
        WHEN is_late_delivery = 1 THEN 'Late'
        WHEN is_late_delivery = 0 THEN 'On Time'
        ELSE 'Unknown'
    END AS delivery_status,
    COUNT(DISTINCT order_id) AS total_orders
FROM warehouse.fact_order_items
WHERE order_status = 'delivered'
GROUP BY delivery_status
ORDER BY total_orders DESC;
```

---

## 14. Common Issues and Fixes

### 14.1 Metabase cannot connect to PostgreSQL

Use this inside Metabase:

```text
Host: postgres
Port: 5432
```

Do not use `localhost:5433` inside Metabase because Metabase runs inside Docker.

---

### 14.2 Local Python cannot connect to PostgreSQL

Use this in local `.env`:

```env
DB_HOST=localhost
DB_PORT=5433
```

Local Python runs on Windows, so it connects through the exposed host port.

---

### 14.3 Airflow cannot connect to PostgreSQL

Airflow runs inside Docker, so it must use:

```text
DB_HOST=postgres
DB_PORT=5432
```

---

### 14.4 Cannot drop raw table because staging view depends on it

This happens if raw loading uses:

```python
if_exists="replace"
```

The correct approach is:

```text
TRUNCATE raw table
→ append new data
```

This preserves table dependencies used by staging views.

---

### 14.5 dbt debug fails because of git permission in Airflow

`dbt debug` can fail in Airflow if the container user cannot run `git`.

The production DAG does not need `dbt debug`. Use:

```text
load_raw_data → dbt_run → dbt_test → data_quality_check
```

---

## 15. Key Learnings

Through this project, I practiced:

- Building an end-to-end batch ELT pipeline
- Loading raw CSV data into PostgreSQL
- Organizing data into raw, staging, and warehouse layers
- Modeling fact and dimension tables using a star schema
- Using dbt for SQL-based transformations and tests
- Writing Python data quality checks
- Building business dashboards with Metabase
- Orchestrating pipeline tasks with Airflow
- Running a multi-service data stack with Docker Compose
- Debugging real-world issues such as Docker networking, database dependencies, and environment variables

---

## 16. Future Improvements

Possible improvements:

- Add incremental loading instead of full truncate-and-append
- Add dbt incremental models
- Add data lineage documentation with dbt docs
- Add GitHub Actions for CI checks
- Add Great Expectations or Soda for stronger data validation
- Store raw data in MinIO/S3 before loading into PostgreSQL
- Build a custom Airflow Docker image instead of using `_PIP_ADDITIONAL_REQUIREMENTS`
- Add alerting for failed Airflow tasks
- Deploy the pipeline to a cloud platform
- Add a Makefile for simpler commands

---

## 17. Portfolio Summary

This project demonstrates the ability to build a complete Data Engineering pipeline from raw data ingestion to analytics-ready data models, data quality validation, dashboarding, and orchestration.

It covers the core skills required for a Data Engineer intern/fresher role:

```text
Python
SQL
PostgreSQL
dbt
Airflow
Docker
Metabase
Data Warehouse
Data Modeling
Data Quality
Pipeline Orchestration
```
---

## 18. GitHub Topics

Recommended GitHub repository topics:

```text
data-engineering
etl
elt
airflow
dbt
postgresql
docker
metabase
data-warehouse
data-pipeline
python
sql
analytics-engineering
```

These topics help recruiters and other developers quickly understand the project stack.

