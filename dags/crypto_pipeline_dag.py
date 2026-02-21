from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator  # type: ignore
import sys
import os

# Adiciona o diretório raiz ao PYTHONPATH para conseguir importar os módulos src
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.extract import fetch_crypto_data
from src.load import load_data_to_postgres

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2026, 2, 20),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'crypto_pipeline',
    default_args=default_args,
    description='Pipeline ETL de criptomoedas (CoinGecko -> PostgreSQL)',
    schedule_interval='*/5 * * * *',   # a cada 5 minutos,          
    catchup=False,
    tags=['crypto'],
)

def run_pipeline(**context):
    """
    Função que executa a extração e a carga.
    Levanta exceção se algo falhar, fazendo a tarefa ser marcada como failed.
    """
    df = fetch_crypto_data()
    if df is None or df.empty:
        raise ValueError("Extração falhou ou retornou nenhum dado.")
    load_data_to_postgres(df, 'precos_crypto')
    return "Pipeline executado com sucesso."

tarefa_pipeline = PythonOperator(
    task_id='executa_pipeline_etl',
    python_callable=run_pipeline,
    dag=dag,
)