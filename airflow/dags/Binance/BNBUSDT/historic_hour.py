import sys
import os

# Add 'utils' directory to the Python path
sys.path.append('/opt/airflow/dags/utils/')

from utils import api_request_get_asset_from_asset_id, get_last_timestamp, get_data_from_api, upload_prices, get_full_prices_past, create_df_extra_assets_data, upload_indicators

from datetime import datetime , timedelta
import pandas as pd

from airflow import DAG
from airflow.operators.python import PythonVirtualenvOperator, PythonOperator
from airflow.operators.dummy import DummyOperator


EXCHANGE_ID = "e47be64c-3398-404f-878f-b5a5009a8f25"
BNBUSDT_HOUR_ID = "171b0da9-caf5-4974-968c-a1061898f5a8"


def main():

    base_url = "http://172.24.100.128:5000/"

    ASSET_ID = BNBUSDT_HOUR_ID
    
    print("asset: "+ASSET_ID)

    final_timestamp = int(datetime.now().timestamp())

    # # Get the asset from the API
    asset = api_request_get_asset_from_asset_id(base_url,EXCHANGE_ID,ASSET_ID)


    # Get the last recorded price timestamp for the specified asset ID
    last_timestamp , first_report  = get_last_timestamp(base_url,ASSET_ID,asset["interval"].iloc[0])

    # Get the prices from the BINANCE API
    df_prices_final = get_data_from_api(symbol=asset["symbol"].iloc[0], interval=asset["interval"].iloc[0], initial_timestamp=last_timestamp, limit_timestamp=final_timestamp)

    # Upload the prices to the API
    upload_prices(df_prices_final,base_url,ASSET_ID)

    df_with_indicators = get_full_prices_past( base_url, ASSET_ID, asset["interval"].iloc[0], last_timestamp, first_report,final_timestamp)

    df_extra_assets_data = create_df_extra_assets_data(start_date=last_timestamp, end_date=final_timestamp)

    df_final = pd.merge(df_with_indicators, df_extra_assets_data , on='timestamp_round_day', how='left')

    df_final.drop(['timestamp_round_day'], axis=1, inplace=True)

    upload_indicators(df_final,base_url)


default_args = {
    'owner': 'Julian Oliveros',
    'depends_on_past': False,
    'email': ['je.oliverosf@uniandes.edu.co'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=5),
    'start_date': datetime(2021, 1, 30),
    # 'on_failure_callback':send_error
}


with DAG(
     	dag_id ="BNBUSDT_historic_hour",
        default_args = default_args,
		description="Upload information of BNBUSDT historic with hour interval",
		schedule_interval="0 */6 * * *",
		catchup = False,
        tags = ['BNBUSDT', 'hour']

) as dag:
        
	start = DummyOperator(task_id="start") 


	upload_prices_data = PythonOperator(
				task_id ="upload_prices_data",
				python_callable = main,
                dag=dag)

	end = DummyOperator(task_id="end") 

	start >> upload_prices_data >> end