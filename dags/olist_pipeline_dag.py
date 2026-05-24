from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator


PROJECT_DIR = "/opt/airflow/project"
DBT_DIR = f"{PROJECT_DIR}/dbt_project/olist_dbt"


default_args = {
    "owner": "khanh",
    "retries": 1,
}


with DAG(
    dag_id="olist_ecommerce_data_pipeline",
    description="End-to-end Olist ecommerce data pipeline",
    default_args=default_args,
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    tags=["data-engineering", "dbt", "postgres", "olist"],
) as dag:

    check_project_files = BashOperator(
        task_id="check_project_files",
        bash_command=f"""
        echo "Checking project files..."
        ls -la {PROJECT_DIR}
        ls -la {PROJECT_DIR}/scripts
        ls -la {DBT_DIR}
        """,
    )

    load_raw_data = BashOperator(
        task_id="load_raw_data",
        bash_command=f"""
        cd {PROJECT_DIR}
        python scripts/load_raw_data.py
        """,
    )

    dbt_debug = BashOperator(
        task_id="dbt_debug",
        bash_command=f"""
        cd {DBT_DIR}
        dbt debug --profiles-dir .
        """,
    )

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command=f"""
        cd {DBT_DIR}
        dbt run --profiles-dir .
        """,
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command=f"""
        cd {DBT_DIR}
        dbt test --profiles-dir .
        """,
    )

    data_quality_check = BashOperator(
        task_id="data_quality_check",
        bash_command=f"""
        cd {PROJECT_DIR}
        python scripts/data_quality.py
        """,
    )

    check_project_files >> load_raw_data >> dbt_debug >> dbt_run >> dbt_test >> data_quality_check