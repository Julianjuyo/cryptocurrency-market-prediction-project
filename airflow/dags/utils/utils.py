
from datetime import datetime, timezone
import pandas as pd
import requests
import json
import math
import yfinance as yf
from joblib import Parallel, delayed


BINANCE_URL = 'https://api.binance.com/api/v3/klines'

NUM_CORES = 6

PROXIES = {
    'http': 'http://discproxy.virtual.uniandes.edu.co:443',
}

# Method to make API request to retrieve the last recorded price timestamp for a given asset ID


def api_request_last_time_stamp_from_asset_id(base_url, asset_id):
    # try:
    print("entro api_request_last_time_stamp_from_asset_id")

    # Make GET request to API endpoint
    response = requests.get(base_url + "assets/" +
                            asset_id + "/last_price/", proxies=PROXIES)

    # Check if the request was successful
    if response.status_code == requests.codes.ok:

        print("get las unix time status code: "+str(response.status_code))

        # Convert JSON response to Python dictionary
        json_data = json.loads(response.content)
        # Normalize the dictionary and convert it to a Pandas DataFrame
        df = pd.json_normalize(json_data)
        # Return the Unix timestamp of the last recorded price for the specified asset ID
        return int(df['unix_time'].iloc[0])
    else:
        print("fallo")
        print(response.content)
        json_data = json.loads(response.content)
        df = pd.json_normalize(json_data)
        return df
    # except:
    #     print("Failed api_request_last_time_stamp_from_asset_id")

# Method to make a GET request to the API endpoint


def api_request_get_asset_from_asset_id(base_url, exchange_id, asset_id):
    # try:
    # Make GET request to API endpoint

    response = requests.get(base_url + "exchanges/" +
                            exchange_id + "/asset/"+asset_id, proxies=PROXIES)

    # Check if the request was successful
    if response.status_code == requests.codes.ok:
        print("get asset status code: "+str(response.status_code))
        # Convert JSON response to Python dictionary
        json_data = json.loads(response.content)
        # Normalize the dictionary and convert it to a Pandas DataFrame
        df = pd.json_normalize(json_data)
        # Return the Unix timestamp of the last recorded price for the specified asset ID

        print("symbol: " + df["symbol"].iloc[0])
        print("interval: " + df["interval"].iloc[0])
        return df
    else:
        print(response.content)
        json_data = json.loads(response.content)
        df = pd.json_normalize(json_data)
        return df
    # except:
    #     print("Failed api_request_get_asset_from_asset_id")


# Method to make API request to retrieve prices for a given asset ID between two specified Unix timestamps
def api_request_get_prices_between_unix_time(base_url, asset_id, unix_time_start, unix_time_end):

    print("entro api_request_get_prices_between_unix_time")

    # try:
    # Make GET request to API endpoint with query parameters for start and end Unix timestamps
    response = requests.get(base_url + "assets/" + asset_id + "/indicators_unix_between/",
                            params={'unix_time_start': unix_time_start, 'unix_time_end': unix_time_end}, proxies=PROXIES)

    print("status code time between: " + str(response.status_code))

    # Check if the request was successful
    if response.status_code == requests.codes.ok:
        print("get prices between status code: "+str(response.status_code))
        # Convert JSON response to Python dictionary
        json_data = json.loads(response.content)
        # Normalize the dictionary and convert it to a Pandas DataFrame
        df = pd.json_normalize(json_data)
        # Return the DataFrame containing the retrieved price data
        return df

    else:
        print("Failed api_request_get_prices_between_unix_time")
        json_data = json.loads(response.content)

        print(json_data)
        return json_data

    # except:
    #     print("Failed api_request_get_prices_between_unix_time")


# Method to make a POST request to the specified API endpoint with a JSON payload
def post_method(url_path, data_dict):
    # Convert the dictionary to a JSON string using the `json` module
    json_payload = json.dumps(data_dict)
    # print("data : "+json_payload)

    # try:
    # Send the POST request with the JSON payload
    response = requests.post(url_path, data=json_payload, proxies=PROXIES)

    # Check if the request was successful
    if response.status_code == requests.codes.created:
        # If successful, print the response content and convert it to a Pandas DataFrame
        # print("post status code: " + str(response.status_code))

        # print(response.content)
        json_data = json.loads(response.content)
        df = pd.json_normalize(json_data)
        return df
    else:
        # If unsuccessful, print the response content
        print("post status code: "+str(response.status_code))
        print("failed: "+json_payload)
        print(response.content)

    # except:
    #     # If an exception occurs, print an error message
    #     print("Failed to make request")

# Method to create a new price for a given asset ID


def create_price_to_asset_id(base_url, asset_id, data_dict):
    # Call the `post_method` function with the appropriate URL and data dictionary
    return post_method(base_url + "assets/" + asset_id + "/prices/", data_dict)

# Method to create a new indicator for a given price ID


def create_indicator_to_price_id(base_url, data_dict):

    price_id = data_dict['id']
    del data_dict['id']

    # Iterate over the keys of the dictionary
    for key in list(data_dict.keys()):
        # Check if the value of the key is NaN
        if math.isnan(data_dict[key]):
            # Delete the key-value pair from the dictionary
            del data_dict[key]

    # Call the `post_method` function with the appropriate URL and data dictionary
    return post_method(base_url + "prices/" + price_id + "/indicators/", data_dict)


def round_minute(epoch_timestamp):
    # convert epoch timestamp to datetime object
    timestamp1 = datetime.utcfromtimestamp(epoch_timestamp)

    # round to nearest day
    rounded_timestamp1 = timestamp1.replace(
        second=0, microsecond=0, tzinfo=timezone.utc)

    # convert rounded timestamp back to epoch timestamp
    return int(rounded_timestamp1.timestamp())


def round_hour(epoch_timestamp):
    # convert epoch timestamp to datetime object
    timestamp2 = datetime.utcfromtimestamp(epoch_timestamp)

    # round to nearest hour
    rounded_timestamp2 = timestamp2.replace(
        minute=0, second=0, microsecond=0, tzinfo=timezone.utc)

    # convert rounded timestamp back to epoch timestamp
    return int(rounded_timestamp2.timestamp())


def round_day(epoch_timestamp):
    # convert epoch timestamp to datetime object
    timestamp3 = datetime.utcfromtimestamp(epoch_timestamp)

    # round to nearest day
    rounded_timestamp3 = timestamp3.replace(
        hour=0, minute=0, second=0, microsecond=0, tzinfo=timezone.utc)

    # convert rounded timestamp back to epoch timestamp
    return int(rounded_timestamp3.timestamp())


def get_data_from_api(
        symbol: str, interval: str, initial_timestamp: int, limit_timestamp: int):
    """ This function get the information from binance API
    """

    # Set working dates ------------------------------------------------------------------------------------
    # End of Looping Period Date
    # Load will go from initial_date to limit_date
    # Start date is inclusive

    # set fields
    fields = ['datetime', 'open', 'high', 'low', 'close', 'volume', 'close_time',
              'qav', 'num_trades', 'taker_base_vol', 'taker_quote_vol', 'ignore']

    counter = 0
    df_prices = pd.DataFrame(columns=fields)

    if interval == "minute":

        initial_timestamp = round_minute(initial_timestamp)
        limit_timestamp = round_minute(limit_timestamp)

        print("last time in the api: " +
              str(datetime.utcfromtimestamp(initial_timestamp)))
        print("Actual datetime: " + str(datetime.utcfromtimestamp(limit_timestamp)))

        if initial_timestamp + 60 < limit_timestamp:
            print("Si se trae data")
            initial_timestamp = initial_timestamp + 60
            limit_timestamp = limit_timestamp - 62
        else:
            print("Finalizo y no hay datos")
            return df_prices

        interval_binance = "1m"
        limit_binance = "960"
        following_period = 57600

        # We will work with time intervals of 16 hours when working with minutes to have 960 records per API call - LIMIT = 1000
        end_date_timestamp = initial_timestamp + following_period

    if interval == "hour":

        initial_timestamp = round_hour(initial_timestamp)
        limit_timestamp = round_hour(limit_timestamp)

        print("last time in the api: " +
              str(datetime.utcfromtimestamp(initial_timestamp)))
        print("Actual datetime: " + str(datetime.utcfromtimestamp(limit_timestamp)))

        if initial_timestamp + 3600 < limit_timestamp:
            print("Si se trae data")
            initial_timestamp = initial_timestamp + 3600
            limit_timestamp = limit_timestamp - 3602
        else:
            print("Finalizo y no hay datos")
            return df_prices

        interval_binance = "1h"
        limit_binance = "960"
        following_period = 144000

        # We will work with time intervals of 40 days when working with hours to have 960 records per API call - LIMIT = 1000
        end_date_timestamp = initial_timestamp + following_period

    if interval == "day":

        initial_timestamp = round_day(initial_timestamp)
        limit_timestamp = round_day(limit_timestamp)

        print("last time in the api: " +
              str(datetime.utcfromtimestamp(initial_timestamp)))
        print("Actual datetime: " + str(datetime.utcfromtimestamp(limit_timestamp)))

        if initial_timestamp + 86400 < limit_timestamp:
            print("Si se trae data")
            initial_timestamp = initial_timestamp + 86400
            limit_timestamp = limit_timestamp - 86402
        else:
            print("Finalizo y no hay datos")
            return df_prices

        interval_binance = "1d"
        limit_binance = "360"
        following_period = 31104000
        end_date_timestamp = initial_timestamp + following_period

    # Start time of function
    loop_start_time = datetime.now()

    # Loop through API calls ---------------------------------------------------------------------------
    while initial_timestamp < limit_timestamp:
        print("Entro loop")

        # Set dates to Binance API format
        start = str(initial_timestamp*1000)

        if end_date_timestamp > limit_timestamp:
            end = str(limit_timestamp*1000)
        else:
            end = str(end_date_timestamp*1000)

        par = {'symbol': symbol, 'interval': interval_binance,
               'startTime': start, 'endTime': end, 'limit': limit_binance}

        # API CALL
        response = requests.get(BINANCE_URL, params=par)
        json_data = json.loads(response.content)
        new_df = pd.DataFrame(json_data, columns=fields)
        df_prices = pd.concat([df_prices, new_df], axis=0)

        # Move to following period
        initial_timestamp = end_date_timestamp
        end_date_timestamp = initial_timestamp + following_period
        counter += 1

    # End time of function
    loop_end_time = datetime.now()

    time = loop_end_time - loop_start_time

    df_prices = df_prices.drop_duplicates()
    
    print('DONE', '\nDURATION:', time.days, 'DAYS', time.seconds//3600, 'HOURS',
          (time.seconds//60) % 60, 'MINUTES', time.seconds % 60, 'SECONDS.')
    print('API CALLS:', counter, ' ROWS:', len(df_prices))

    df_prices = df_prices.rename(columns={'datetime': 'unix_time',
                                          'open': 'open_price',
                                          'high': 'high_price',
                                          'low': 'low_price',
                                          'close': 'close_price'})

    df_prices['unix_time'] = df_prices['unix_time'].apply(
        lambda x: int(round(x / 1000)))
    
    

    return df_prices


def get_last_timestamp(base_url, asset_id, interval):

    last_timestamp_response = api_request_last_time_stamp_from_asset_id(
        base_url, asset_id)

    last_timestamp = None
    first_report = None

    if isinstance(last_timestamp_response, int):
        first_report = False
        last_timestamp = last_timestamp_response
    else:
        if last_timestamp_response["error message"].iloc[0] == "There are not prices for this asset":
            print("There are not prices for this asset")

            first_report = True

            if interval == "minute":
                last_timestamp = 1675123200  # 31 of enero 2023
            if interval == "hour":
                last_timestamp = 1672099200  # 26 of dicember 2022
            if interval == "day":
                last_timestamp = 1661904000  # 31 of august 2022

        elif last_timestamp_response["error message"].iloc[0] == "The Asset with the given id was not found":
            print("The Asset with the given id was not found")
            last_timestamp = None

    return last_timestamp, first_report


def upload_prices(df_prices, base_url, asset_id):

    if df_prices.empty:
        print("There are NO prices to upload")
    else:
        print("There are prices to upload")

        # make multiple POST requests in parallel using joblib
        num_cores = NUM_CORES  # number of CPU cores to use
        # convert dataframe to list of dictionaries
        data_list = df_prices.to_dict('records')
        results = Parallel(n_jobs=num_cores)(delayed(create_price_to_asset_id)(
            base_url, asset_id, data) for data in data_list)

    print("DONE upload_prices")


# Define a function to convert Unix timestamp to date string
# def unix_to_date(unix_timestamp):
#     datetime_obj = datetime.utcfromtimestamp(unix_timestamp)
#     date_str = datetime_obj.date().strftime('%Y-%m-%d')
#     return date_str


# Method to get
def get_full_prices_past(base_url, asset_id, interval, last_timestamp, first_report, final_timestamp):

    if first_report:
        print("first report")
        first_indicator_time = last_timestamp
        timestamp_to_add = last_timestamp

    else:
        if interval == "minute":
            first_indicator_time = last_timestamp - 6000
            timestamp_to_add = last_timestamp - 60

        if interval == "hour":
            first_indicator_time = last_timestamp - 360000
            timestamp_to_add = last_timestamp - 3600
        if interval == "day":
            first_indicator_time = last_timestamp - 8640000
            timestamp_to_add = last_timestamp - 86400

    df_prices = api_request_get_prices_between_unix_time(
        base_url, asset_id, first_indicator_time, final_timestamp)

    df_prices_wit_indicators = df_prices  # add_indicators(df_prices)

    df_prices_wit_indicators.drop(['low_price', 'asset_id', 'updated_at', 'high_price', 'volume', 'date_time_utc', 'qav', 'date_time_gmt_5',
                                  'num_trades', 'open_price', 'taker_base_vol', 'close_price', 'taker_quote_vol', 'created_at', 'ignore'], axis=1, inplace=True)

    df_prices_wit_indicators = df_prices_wit_indicators.loc[
        df_prices_wit_indicators['unix_time'] >= timestamp_to_add]

    # Apply the function to the 'unix_timestamp' column and create a new column called 'date'
    df_prices_wit_indicators['timestamp_round_day'] = df_prices_wit_indicators['unix_time'].apply(
        round_day)

    return df_prices_wit_indicators


# Method to post the indicators to the API
def upload_indicators(df_with_indicators, base_url):

    print("uploading indicators")

    # loop through all rows and convert each row to a JSON object

    num_cores = NUM_CORES  # number of CPU cores to use
    # convert dataframe to list of dictionaries
    data_list = df_with_indicators.to_dict('records')

    results = Parallel(n_jobs=num_cores)(
        delayed(create_indicator_to_price_id)(base_url, data) for data in data_list)

    print("DONE upload_indicators")


def get_extra_assets_data(start_date, end_date, name, ticker):

    print("Getting data for: " + name + " "+ticker)

    df = yf.Ticker(ticker).history(
        interval="1d", start=start_date, end=end_date)
    df = df.reset_index(drop=False)

    # df['date']= df['Date'].dt.date

    df['unix_time'] = df['Date'].dt.date.apply(
        lambda x: int(pd.Timestamp(x).timestamp()))

    # Apply the function to the 'unix_timestamp' column and create a new column called 'date'
    df['timestamp_round_day'] = df['unix_time'].apply(round_day)

    df.drop(['Open', 'High', 'Low', 'Volume', 'Dividends',
            'Stock Splits', 'Date', 'unix_time'], axis=1, inplace=True)

    df.rename(columns={'Close': name}, inplace=True)

    print("DONE getting data for" + name + " "+ticker)
    return df


def create_df_extra_assets_data(start_date, end_date):

    dict_assets_extra = {
        "gold_price":  "GC=F",
        "silver_price":  "SI=F",
        "natural_gas_price":  "NG=F",
        "cotton_price":  "CT=F",
        "coffee_price":  "KC=F",
        "sugar_price":  "SB=F",
        "cocoa_price":  "CC=F",
        "rice_price":  "ZR=F",
        "corn_price":  "ZC=F",
        "wheat_price":  "KE=F",
        "soybean_price":  "ZS=F",
        "oats_price":  "ZO=F",
        "spy500_price":  "ES=F",
        "dow_jones_price":  "YM=F",
        "nasdaq_price":  "NQ=F",
        "russell_2000_price":  "RTY=F",
        "us_10_year_treasury_price":  "ZN=F",
        "us_5_year_treasury_price":  "ZF=F",
        "us_2_year_treasury_price":  "ZT=F",
        "usbond_price":  "ZB=F"
    }

    df_extra_assets_data = pd.DataFrame()
    count = 0

    for key, value in dict_assets_extra.items():

        if count == 0:
            df_extra_assets_data = get_extra_assets_data(
                start_date, end_date, name=key, ticker=value)

        else:
            df_extra_assets_data = pd.merge(df_extra_assets_data, get_extra_assets_data(
                start_date, end_date, name=key, ticker=value), on='timestamp_round_day', how='outer')

        count += 1

    return df_extra_assets_data
