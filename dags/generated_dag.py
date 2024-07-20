from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
import subprocess

def run_script():
    subprocess.run(['python', '/opt/airflow/dags/generated_code.py'], check=True)

default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1),
    'retries': 1,
}

dag = DAG(
    'generated_dag',
    default_args=default_args,
    description='A simple DAG to run generate_code.py script',
    schedule_interval='* * * * *',
)

run_script_task = PythonOperator(
    task_id='run_script_task',
    python_callable=run_script,
    dag=dag,
)

