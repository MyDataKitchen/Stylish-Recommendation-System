from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from airflow import DAG
from dotenv import load_dotenv
import os

load_dotenv()

default_args = {
  'owner': 'Alfred',
  'start_date': datetime(2022, 5, 28),
  'email': ['mylearning.jiayong@gmail.com'],
  'email_on_failure': False,
  'email_on_retry': False,
  'retries': 3,
  'retry_delay': timedelta(seconds=30)
}

dag = DAG(
    dag_id='recommender_system',
    description='my operator dag',
    default_args=default_args,
    schedule_interval='0 */6 * * *'
)

def extract_reviews_from_database(ti):
    import sys
    import json
    from datetime import datetime
    path = os.getenv('module_path')
    sys.path.insert(0, path)
    from model import get_reviews
    from s3 import put_data_to_s3

    data = get_reviews()
    datetime_now = datetime.now().strftime("%m-%d-%Y_%H:%M:%S")

    bucket = os.getenv('bucket')
    key = 'temp_data/reviews/' + f'reviews_{datetime_now}.json'
    data = json.dumps(data)
    put_data_to_s3(bucket, key, data)
    ti.xcom_push(key='temp_reviews', value=key)


def build_model(ti):
    import sys
    import io
    import pandas as pd
    path = os.getenv('module_path')
    sys.path.insert(0, path)
    from similarity import items_rating, users_rating, combinations, items_cosine_similarity_calculation
    from s3 import put_data_to_s3, get_json_from_s3
    from datetime import datetime

    bucket = os.getenv('bucket')
    key = ti.xcom_pull(key='temp_reviews', task_ids='extract_reviews_task')

    data = get_json_from_s3(bucket, key)

    items = items_rating(data)
    users = users_rating(data)
    combinations = combinations(items, users)
    cosine_similarity = items_cosine_similarity_calculation(items, combinations)
    df = pd.DataFrame(cosine_similarity)

    datetime_now = datetime.now().strftime("%m-%d-%Y_%H:%M:%S")
    key = 'temp_data/similarity/' + f'df_similarity_{datetime_now}.pkl'

    pickle_buffer = io.BytesIO()
    df.to_pickle(pickle_buffer)
    put_data_to_s3(bucket, key, pickle_buffer.getvalue())

    ti.xcom_push(key='similarity', value=key)

def load_model_to_sql(ti):
    import sys
    path = os.getenv('module_path')
    sys.path.insert(0, path)
    from model import dataframe_to_sql
    from s3 import get_dataframe_from_s3

    bucket = os.getenv('bucket')
    key = ti.xcom_pull(key='similarity', task_ids='build_model_task')
    df = get_dataframe_from_s3(bucket, key)
    dataframe_to_sql("similarity", df)


extract_reviews_task = PythonOperator(
    task_id='extract_reviews_task',
    python_callable=extract_reviews_from_database,
    dag=dag,
    do_xcom_push=True
)

build_model_task = PythonOperator(
    task_id='build_model_task',
    python_callable=build_model,
    dag=dag,
    do_xcom_push=True
)

load_model_task = PythonOperator(
    task_id='load_model_task',
    python_callable=load_model_to_sql,
    dag=dag,
    do_xcom_push=False
)

extract_reviews_task >> build_model_task >> load_model_task