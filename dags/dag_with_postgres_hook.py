from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.postgres_operator import PostgresOperator
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
import csv
import logging


args = {
    'owner': 'mikhailok',
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}


def get_data(execution_date, next_execution_date):
    hook = PostgresHook(postgres_conn_id="original_database")
    conn = hook.get_conn()
    cursor = conn.cursor()
    cursor.execute("select * from band_t")
    with open(f"dag/get_data_{execution_date}.txt", "w") as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow([i[0] for i in cursor.descritption])
        csv_writer.writerows(cursor)
    cursor.close()
    conn.close()
    logging.info("Saved bands data in text file")


with DAG (dag_id='dag_with_postgres_hooks_V2', default_args=args, start_date=datetime(2018, 11, 1), schedule_interval='@daily') as dag:
    task_1_get_data = PythonOperator(
	    task_id='get_data',
	    python_callable=get_data
    )

    task_1_get_data