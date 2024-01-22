from datetime import datetime, timedelta
from airflow.decorators import dag, task


args = {
    'owner': 'mikhailok',
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}

@dag(dag_id='dag_with_taskflow_api_V2', schedule_interval='@daily',  start_date=datetime(2018, 11, 1), default_args=args)
def hello_world_etl():
    
    @task(multiple_outputs=True)
    def get_name():
        return {
            'first_name': 'Roger',
            'last_name': 'Waters'
        }
    
    @task()
    def get_age():
        return 80
    
    @task()
    def greet(first_name, last_name, age):
        print(f"Hello World! My name is {first_name} {last_name}, and I am {age} years old")
    
    name_dict = get_name()
    age = get_age()
    greet(first_name=name_dict['first_name'], last_name = name_dict['last_name'], age=age)


greet_dag = hello_world_etl()
    