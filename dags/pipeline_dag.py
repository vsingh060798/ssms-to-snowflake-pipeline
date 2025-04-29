# pipeline_dag.py
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.providers.http.sensors.http import HttpSensor
from airflow.providers.http.operators.http import SimpleHttpOperator

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.operators.http_operator import SimpleHttpOperator
from airflow.utils.dates import days_ago
from datetime import timedelta

default_args = {
    'owner': 'vishwas',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='ssms_to_snowflake_pipeline',
    default_args=default_args,
    description='Extract from SQL Server and Load into Snowflake with DBT Trigger',
    schedule_interval='@daily',   # you can adjust later
    start_date=days_ago(1),
    catchup=False,
    tags=['project', 'snowflake', 'dbt']
) as dag:

    # Task 1: Extract Data
    extract_data = BashOperator(
        task_id='extract_data',
        bash_command='cd /opt/airflow/dags/ && python src/extract.py'
    )

    # Task 2: Load Data
    load_data = BashOperator(
        task_id='load_data',
        bash_command='cd /opt/airflow/dags/ && python src/load.py'
    )

    # Task 3: Insert Audit Log
    insert_audit_log = BashOperator(
        task_id='insert_audit_log',
        bash_command='cd /opt/airflow/dags/ && python src/audit.py'
    )
    
    # Task 4: 
    trigger_dbt_job = SimpleHttpOperator(
    task_id='trigger_dbt_job',
    http_conn_id='dbt_cloud_default',
    endpoint='api/v2/accounts/70471823454138/jobs/70471823458111/run/',
    method='POST',
    headers={"Content-Type": "application/json"},
    response_check=lambda response: True if response.status_code == 200 else False,
    retries=1,                                
    retry_delay=timedelta(seconds=30),         
    dag=dag
)

    extract_data >> load_data >> insert_audit_log >> trigger_dbt_job
