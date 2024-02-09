from datetime import datetime, timedelta
from airflow import DAG
from airflow.models.dag import DAG
from airflow.decorators import dag, task
from airflow.utils.task_group import TaskGroup
from airflow.providers.postgres.hooks.postgres import PostgresHook
import csv
import logging
import os
import pathlib



args = {
    'owner': 'mikhailok'
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
def load_src_data(tbl_dict):
    for k, v in tbl_dict['table_name'].items():
        hook = PostgresHook(postgres_conn_id="orig_db")
        sql = f'SELECT * FROM {v}'
        conn = hook.get_conn()
        cursor = conn.cursor()
        cursor.execute(sql)
        
        exp_dir = "{}/exp-dir".format(os.getcwd())
        if not os.path.isdir(exp_dir):
            print('Exporting directory not exist. Creating')
            os.mkdir(exp_dir)
        export_path = "{}/src_data_{}.csv".format(exp_dir, v)
        with open(export_path, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([i[0] for i in cursor.description])
            csv_writer.writerows(cursor)
        cursor.close()
        conn.close()
        logging.info(f"Saved data from table {v} in csv file")


@task()
def upload_data(tbl_dict):
    for k, v in tbl_dict['table_name'].items():
        hook = PostgresHook(postgres_conn_id="copy_db")
        try:
            exp_dir = "{}/exp-dir".format(os.getcwd())
            export_path = "{}/src_data_{}.csv".format(exp_dir, v)
            sql = f"COPY {v} FROM '{export_path}' DELIMITER ',' CSV HEADER"
            print(sql)

            conn = hook.get_conn()
            cursor = conn.cursor()
            cursor.execute(sql)
            cursor.close()
            conn.close()
            logging.info(f"Saved data from table {v} in new table")
        except:
            print("{}/exp-dir".format(os.getcwd()))
            logging.info("Something wrong in path")
        


# schedule's setting: crontab.guru
with DAG (dag_id='dag_for_migration', default_args=args, start_date=datetime(2024, 2, 2), schedule_interval='*/30 * * * */1') as dag:
    with TaskGroup("extract_and_load", tooltip="Extract and load source data") as extract_load_src:
        src_tables = get_src_tables()
        load_tables = load_src_data(src_tables)

        src_tables >> load_tables
    
    with TaskGroup("upload_data", tooltip="Upload data to copy database") as upload_src_data:
        names_of_tables = get_src_tables()
        upload_all_data = upload_data(names_of_tables)

        names_of_tables >> upload_all_data

    extract_load_src >> upload_src_data