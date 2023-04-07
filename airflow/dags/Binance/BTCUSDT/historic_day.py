import sys
# Add 'data-loader' directory to the Python path
sys.path.append('airflow/dags')

from datetime import datetime , timedelta
from utils import *
import os


from airflow import DAG
from airflow.operators.python import PythonVirtualenvOperator, PythonOperator
from airflow.operators.dummy import DummyOperator



EXCHANGE_ID = "979f24c6-0c23-4158-aaa8-770febb76d9a"
ASSET_ID = "276a8657-e718-4bef-a997-dd8daee9fcc4"



def main():
    #To know if im in a docker enviroment or not
    ON_DOCKER = os.environ.get('ON_DOCKER', False)

    # if ON_DOCKER:
    #     base_url = "http://fastapi:5000/"
    # else:
    
    base_url = "http://0.0.0.0:5000/"

    # Get the asset from the API
    asset = api_request_get_asset_from_asset_id(base_url,EXCHANGE_ID,ASSET_ID)

    print(asset)

    # Get the last recorded price timestamp for the specified asset ID
    last_timestamp = get_last_timestamp(base_url,ASSET_ID)

    # Get the prices from the BINANCE API
    df_prices_final = get_data_from_api(symbol=asset["symbol"].iloc[0], interval=asset["interval"].iloc[0], initial_timestamp=last_timestamp, limit_timestamp=datetime.now().timestamp())

    # Upload the prices to the API
    upload_prices(df_prices_final,base_url,ASSET_ID)

default_args = {
    'owner': 'Julian Oliveros',
    'depends_on_past': False,
    'email': ['je.oliverosf@uniandes.edu.co'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'start_date': datetime(2021, 1, 30),
    # 'on_failure_callback':send_error
}



with DAG(
     	dag_id ="BTCUSDT_historic_day",
        default_args = default_args,
		description="Upload information of BTCUSDT historic with day interval",
		schedule_interval="@once",
		catchup = False,
        tags = ['BTCUSDT', 'day']

		
) as dag:
        
	start = DummyOperator(task_id="start") 


	upload_prices = PythonOperator(
				task_id ="upload_prices",
				python_callable = main,
                dag=dag)

	end = DummyOperator(task_id="end") 

	start >> upload_prices >> end