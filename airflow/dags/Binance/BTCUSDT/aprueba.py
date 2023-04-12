import sys
# Add 'data-loader' directory to the Python path
sys.path.append('airflow/dags') 

from datetime import datetime
from utils import *
import os

EXCHANGE_ID = "979f24c6-0c23-4158-aaa8-770febb76d9a"
ASSET_ID = "276a8657-e718-4bef-a997-dd8daee9fcc4"

def main():
    #To know if im in a docker enviroment or not
    ON_DOCKER = os.environ.get('ON_DOCKER', False)

    if ON_DOCKER:
        base_url = "http://fastapi:5000/"
    else:
        base_url = "http://0.0.0.0:5000/"

    final_timestamp = int(datetime.now().timestamp())


    # Get the asset from the API
    asset = api_request_get_asset_from_asset_id(base_url,EXCHANGE_ID,ASSET_ID)

    # Get the last recorded price timestamp for the specified asset ID
    last_timestamp , first_report  = get_last_timestamp(base_url,ASSET_ID,asset["interval"].iloc[0])

    # Get the prices from the BINANCE API
    df_prices_final = get_data_from_api(symbol=asset["symbol"].iloc[0], interval=asset["interval"].iloc[0], initial_timestamp=last_timestamp, limit_timestamp=final_timestamp)

    # Upload the prices to the API
    upload_prices(df_prices_final,base_url,ASSET_ID)

    df_with_indicators = get_full_prices_past( base_url, ASSET_ID, asset["interval"].iloc[0], last_timestamp, first_report,final_timestamp)


    df_extra_assets_data = create_df_extra_assets_data(start_date=last_timestamp, end_date=final_timestamp)

    df_final = pd.merge(df_with_indicators, df_extra_assets_data , on='timestamp_round_day', how='outer')

    upload_indicators(df_final,base_url,ASSET_ID)





if __name__ == "__main__":

    main()




