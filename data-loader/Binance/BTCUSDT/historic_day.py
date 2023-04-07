import sys
# Add 'data-loader' directory to the Python path
sys.path.append('data-loader') 

from datetime import datetime
from utils import *
import os

EXCHANGE_ID = "90897ad3-1fd0-4199-b0c1-604136910835"
ASSET_ID = "c17d94fd-995e-4a97-a85c-04ae2e4e3915"

def main():
    #To know if im in a docker enviroment or not
    ON_DOCKER = os.environ.get('ON_DOCKER', False)

    if ON_DOCKER:
        base_url = "http://fastapi:5000/"
    else:
        base_url = "http://0.0.0.0:5000/"

    # Get the asset from the API
    asset = api_request_get_asset_from_asset_id(base_url,EXCHANGE_ID,ASSET_ID)

    # Get the last recorded price timestamp for the specified asset ID
    last_timestamp = get_last_timestamp(base_url,ASSET_ID)

    # Get the prices from the BINANCE API
    df_prices_final = get_data_from_api(symbol=asset["symbol"].iloc[0], interval=asset["interval"].iloc[0], initial_timestamp=last_timestamp, limit_timestamp=datetime.now().timestamp())

    # Upload the prices to the API
    upload_prices(df_prices_final,base_url,ASSET_ID)


if __name__ == "__main__":

    main()




