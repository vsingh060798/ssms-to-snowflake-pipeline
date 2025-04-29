# SSMS to Snowflake Real-World Data Pipeline with Airflow and DBT Cloud

---

## 📄 Project Overview

This project demonstrates a real-world **Data Engineering Pipeline** where:
- Data is extracted from **SQL Server (SSMS)** using **Python**.
- Loaded into **Snowflake** (RAW layer).
- ETL orchestrated using **Apache Airflow** (Dockerized).
- Transformations triggered automatically in **DBT Cloud**.
- Final fact tables built in Snowflake.
- Audit logs captured for every load.

Designed to mirror real-world professional data engineering scenarios.

---

## 📢 Architecture Diagram

**(Static PNG + Animated GIF separately attached)**

```text
SQL Server (SSMS)
   ⬇️
Python Extraction
   ⬇️
Snowflake RAW Tables
   ⬇️
Airflow (DAG Scheduling)
   ⬇️
DBT Cloud (Transformations)
   ⬇️
Final Fact Tables
```

---

## 🔗 Technologies Used
- SQL Server (SSMS)
- Python (pyodbc, pandas, snowflake-connector)
- Snowflake Data Warehouse
- Apache Airflow (Dockerized)
- DBT Cloud
- GitHub (Version Control)

---

## 📁 Project Folder Structure

```plaintext
src/
    extract.py
    load.py
    audit.py
    dbt_trigger.py
config_pipeline/
    sqlserver_config.json
    snowflake_config.json
dags/
    pipeline_dag.py
models/
    staging/
        schema.yml
        stg_players.sql
        stg_matches.sql
        stg_player_stats.sql
    facts/
        fct_performance.sql
.gitignore
README.md
docker-compose.yml
```

---

## 📖 How to Set Up This Project

### 1. SQL Server
- Create source tables and insert sample data.

### 2. Python Scripts
- `extract.py`: Pull data from SQL Server.
- `load.py`: Push to Snowflake with `create table if not exists` logic.
- `audit.py`: Insert audit log record after every load.
- `dbt_trigger.py`: Trigger DBT Cloud job.

### 3. Snowflake
- Create database `WORLD_CUP_DB`, schema `RAW`.
- Create tables if they don't exist automatically (handled in load.py).

### 4. Airflow
- Set up using Docker (Docker Compose).
- DAG: `pipeline_dag.py`
- Tasks:
    - Extract
    - Load
    - Audit
    - Trigger DBT

### 5. DBT Cloud
- Set up transformations:
    - Staging Models
    - Fact Model
- Configure DBT Cloud Job.
- Set API Token for triggering via Airflow.

### 6. GitHub
- Version control all code and configurations.

---

## 🖋️ Airflow DAG Overview

| Task | Description |
|:---|:---|
| extract_data | BashOperator runs `extract.py` |
| load_data | BashOperator runs `load.py` |
| insert_audit_log | BashOperator runs `audit.py` |
| trigger_dbt_job | SimpleHttpOperator calls DBT Cloud API |

---

## 📊 DBT Models

| Model | Purpose |
|:---|:---|
| stg_players.sql | Clean player base data |
| stg_matches.sql | Clean matches info |
| stg_player_stats.sql | Clean player stats |
| fct_performance.sql | Fact table combining all match and player stats |

---

## 📘 Audit Logging
- Every load inserts a record into an Audit Table.
- Tracks load time, record count, success/failure status.

---

## 🚀 About This Project

This end-to-end pipeline demonstrates:
- Source system integration.
- Data movement automation.
- Modern transformation orchestration (DBT triggered by Airflow).
- Real-world best practices: Parameterization, Incremental Loading, Git-based CI/CD, and Audit Tracking.

Designed for:
- Data Engineer roles
- Snowflake Developers
- Cloud Data Pipeline demonstrations

---

## 🌟 Future Enhancements
- Add S3 ingestion option.
- Add email alerting on DAG failures.
- Deploy DBT jobs via GitHub CI/CD pipelines.

---

## 🔗 GitHub Repository

> This project is part of the GitHub repository: **`ssms-to-snowflake-pipeline`**

(Repository link will be added after push.)

---

# ✨ Vishwas Singh - Data Engineer | Real World Project Execution ✨

