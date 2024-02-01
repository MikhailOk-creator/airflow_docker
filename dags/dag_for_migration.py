from datetime import datetime, timedelta
from airflow import DAG
from airflow.models.dag import DAG
from airflow.decorators import dag, task
from airflow.utils.task_group import TaskGroup
from airflow.providers.postgres.hooks.postgres import PostgresHook
import csv
import logging
import os



args = {
    'owner': 'mikhailok',
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}


@task()
def get_src_tables():
    hook = PostgresHook(postgres_conn_id="orig_db")
    sql = """ SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_type='BASE TABLE' """
    df = hook.get_pandas_df(sql)
    print(df)
    tbl_dict = df.to_dict('dict')
    return tbl_dict


@task()
def load_src_data(tbl_dict: dict):
    for k, v in tbl_dict['table_name'].items():
        hook = PostgresHook(postgres_conn_id="orig_db")
        sql = f'SELECT * FROM {v}'
        conn = hook.get_conn()
        cursor = conn.cursor()
        cursor.execute(sql)
        export_path = "{}/src_data_{}.csv".format(os.getcwd(), v)
        with open(export_path, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([i[0] for i in cursor.description])
            csv_writer.writerows(cursor)
        cursor.close()
        conn.close()
        logging.info(f"Saved data from table {v} in csv file")


with DAG (dag_id='dag_for_work', default_args=args, start_date=datetime(2024, 1, 28), schedule_interval='@daily') as dag:
    with TaskGroup("extract_and_load", tooltip="Extract and load source data") as extract_load_src:
        src_tables = get_src_tables()
        load_tables = load_src_data(src_tables)

        src_tables >> load_tables

    extract_load_src