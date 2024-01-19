from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

args = {
    'owner': 'mikhailok',
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}

def greet():
    print("Hello World!")

with DAG(dag_id='dag_with_python', description='The first dag using python operator', schedule_interval='@daily',  start_date=datetime(2024, 10, 1), default_args=args) as dag:
    task1 = PythonOperator(
        task_id='greet',
        python_callable=greet
    )

    task1