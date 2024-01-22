from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

args = {
    'owner': 'mikhailok',
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}


def get_name(ti):
    ti.xcom_push(key='first_name', value='Roger')
    ti.xcom_push(key='last_name', value='Waters')


def get_age(ti):
    ti.xcom_push(key='age', value=80)


def greet(ti):
    first_name = ti.xcom_pull(task_ids='get_name', key='first_name')
    last_name = ti.xcom_pull(task_ids='get_name', key='last_name')
    age = ti.xcom_pull(task_ids='get_age', key='age')
    print(f"Hello World! My name is {first_name} {last_name}, and I am {age} years old")


with DAG(dag_id='dag_with_python_V6', description='The first dag using python operator', schedule_interval='@daily',  start_date=datetime(2018, 11, 1), default_args=args) as dag:
    task1 = PythonOperator(
        task_id='greet',
        python_callable=greet
    )

    task2 = PythonOperator(
        task_id='get_name',
        python_callable=get_name
    )

    task3 = PythonOperator(
        task_id = 'get_age',
        python_callable=get_age,
    )

    [task2, task3] >> task1