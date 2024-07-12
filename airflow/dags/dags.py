from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import timedelta, datetime
from kingbets import fetch_kingbets_data
from livescore import crawl
from merge_data import merge
from post_api import post

default_args = {
    'owner' : 'airflow',
    'start_date' : datetime(2024, 7, 10),
}

dag = DAG(dag_id='livescore', 
        default_args=default_args, 
        schedule_interval='*/2 * * * *', 
        catchup=False
    )

fetch_kingbets = PythonOperator(
    task_id='fetch_kingbets',
    python_callable=fetch_kingbets_data,
    dag=dag
)

fetch_livescore = PythonOperator(
    task_id='fetch_livescore',
    python_callable=crawl,
    dag=dag
)

merge_data = PythonOperator(
    task_id='merge_data',
    python_callable=merge,
    dag=dag
)

post_to_mongodb = PythonOperator(
    task_id='post_to_mongodb',
    python_callable=post,
    dag=dag
)

fetch_kingbets >> fetch_livescore >> merge_data >> post_to_mongodb
