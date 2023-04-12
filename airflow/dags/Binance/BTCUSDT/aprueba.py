import sys
# Add 'data-loader' directory to the Python path
sys.path.append('airflow/dags') 

from datetime import datetime
from utils import *
import os

EXCHANGE_ID = "402f5618-6a78-43ad-b4ee-44b3e65a94a7"
BTCUSDT_DAY_ID = "81d625dd-f73f-4829-a2ff-1d795fbc5b3a"


def main():

    base_url = "http://172.24.100.128:5000/"

    ASSET_ID = BTCUSDT_DAY_ID

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

    df_final = pd.merge(df_with_indicators, df_extra_assets_data , on='timestamp_round_day', how='left')

    df_final.drop(['timestamp_round_day'], axis=1, inplace=True)


    upload_indicators(df_final,base_url)


if __name__ == "__main__":

    main()




