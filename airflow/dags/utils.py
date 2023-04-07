# import binance_extract

from datetime import datetime,timezone
import pandas as pd
import requests
import json

BINANCE_URL = 'https://api.binance.com/api/v3/klines'

# Method to make API request to retrieve the last recorded price timestamp for a given asset ID
def api_request_last_time_stamp_from_asset_id(base_url, asset_id):
    # try:
    print("entro api_request_last_time_stamp_from_asset_id")

    # Make GET request to API endpoint
    response = requests.get(base_url + "assets/" + asset_id + "/last_price/")

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
def api_request_get_asset_from_asset_id(base_url,exchange_id, asset_id):
    # try:
        # Make GET request to API endpoint

    response = requests.get(base_url + "exchanges/" + exchange_id + "/asset/"+asset_id)

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
    # try:
    # Make GET request to API endpoint with query parameters for start and end Unix timestamps
    response = requests.get(base_url + "assets/" + asset_id + "/indicators_unix_between/", params={'unix_time_start': unix_time_start, 'unix_time_end': unix_time_end})

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
        json_data = json.loads(response.content)
        print(json_data)
        return json_data
            
        
    # except:
    #     print("Failed api_request_get_prices_between_unix_time")

# Method to make a POST request to the specified API endpoint with a JSON payload
def post_method(url_path, data_dict):
    # Convert the dictionary to a JSON string using the `json` module
    json_payload = json.dumps(data_dict)
    # try:
        # Send the POST request with the JSON payload
    response = requests.post(url_path, data=json_payload)

    # Check if the request was successful
    if response.status_code == requests.codes.created:
        # If successful, print the response content and convert it to a Pandas DataFrame
        print("post status code: "+ str(response.status_code))
        
        print(response.content)
        json_data = json.loads(response.content)
        df = pd.json_normalize(json_data)
        return df
    else:
        # If unsuccessful, print the response content
        print("post status code: "+str(response.status_code))
        print(response.content)
            
    # except:
    #     # If an exception occurs, print an error message
    #     print("Failed to make request")

# Method to create a new price for a given asset ID
def create_price_to_asset_id(base_url, asset_id, data_dict):
    # Call the `post_method` function with the appropriate URL and data dictionary
    return post_method(base_url + "assets/" + asset_id + "/prices/", data_dict)

# Method to create a new indicator for a given price ID
def create_indicator_to_price_id(base_url, price_id, data_dict):
    # Call the `post_method` function with the appropriate URL and data dictionary
    return post_method(base_url + "prices/" + price_id + "/indicators/", data_dict)



def round_minute(epoch_timestamp):
    # convert epoch timestamp to datetime object
    timestamp1 = datetime.utcfromtimestamp(epoch_timestamp)

    # round to nearest day
    rounded_timestamp1 = timestamp1.replace(second=0, microsecond=0, tzinfo=timezone.utc)

    # convert rounded timestamp back to epoch timestamp
    return int(rounded_timestamp1.timestamp())


def round_hour(epoch_timestamp):
    # convert epoch timestamp to datetime object
    timestamp2 = datetime.utcfromtimestamp(epoch_timestamp)

    # round to nearest hour
    rounded_timestamp2 = timestamp2.replace(minute=0, second=0, microsecond=0, tzinfo=timezone.utc)

    # convert rounded timestamp back to epoch timestamp
    return int(rounded_timestamp2.timestamp())
    
def round_day(epoch_timestamp):
    # convert epoch timestamp to datetime object
    timestamp3 = datetime.utcfromtimestamp(epoch_timestamp)

    # round to nearest day
    rounded_timestamp3 = timestamp3.replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=timezone.utc)

    # convert rounded timestamp back to epoch timestamp
    return int(rounded_timestamp3.timestamp())


def get_data_from_api(
      symbol:str
    , interval:str
    , initial_timestamp:int
    , limit_timestamp:int): 

    """ This function get the information from binance API
    """

    # Set working dates ------------------------------------------------------------------------------------
    # End of Looping Period Date
    # Load will go from initial_date to limit_date
    # Start date is inclusive

    #set fields
    fields = ['datetime', 'open', 'high'
    , 'low', 'close', 'volume','close_time'
    , 'qav', 'num_trades','taker_base_vol'
    , 'taker_quote_vol', 'ignore']

    counter = 0 
    df_prices = pd.DataFrame(columns=fields)


    if interval == "minute":

        initial_timestamp = round_minute(initial_timestamp)
        limit_timestamp = round_minute(limit_timestamp)

        print("last time in the api: " + str(datetime.utcfromtimestamp(initial_timestamp)))
        print("Actual datetime: " +  str(datetime.utcfromtimestamp(limit_timestamp)))

        if initial_timestamp + 60 < limit_timestamp:
            print("Si se trae data")
            initial_timestamp = initial_timestamp + 60
            limit_timestamp = limit_timestamp - 60
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

        print("last time in the api: " + str(datetime.utcfromtimestamp(initial_timestamp)))
        print("Actual datetime: " +  str(datetime.utcfromtimestamp(limit_timestamp)))

        if initial_timestamp + 3600 < limit_timestamp:
            print("Si se trae data")
            initial_timestamp = initial_timestamp + 3600
            limit_timestamp = limit_timestamp - 3600
        else:
            print("Finalizo y no hay datos")
            return df_prices

        interval_binance = "1h"
        limit_binance = "960"
        following_period = 144000

        # We will work with time intervals of 40 days when working with hours to have 960 records per API call - LIMIT = 1000
        end_date_timestamp = initial_timestamp +  following_period

    if interval == "day":

        initial_timestamp = round_day(initial_timestamp)
        limit_timestamp =   round_day(limit_timestamp)
        
        print("last time in the api: " + str(datetime.utcfromtimestamp(initial_timestamp)))
        print("Actual datetime: " +  str(datetime.utcfromtimestamp(limit_timestamp)))
        
        if initial_timestamp + 86400 < limit_timestamp:
            print("Si se trae data")
            initial_timestamp = initial_timestamp + 86400
            limit_timestamp = limit_timestamp - 86400
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
    while initial_timestamp <= limit_timestamp:
        print("Entro loop")
      
        # Set dates to Binance API format
        start = str(initial_timestamp*1000)

        if end_date_timestamp > limit_timestamp:
            end = str(limit_timestamp*1000)
        else :
            end = str(end_date_timestamp*1000)

        par = {'symbol': symbol, 'interval': interval_binance, 'startTime': start, 'endTime': end, 'limit':limit_binance}
        
        # API CALL
        response = requests.get(BINANCE_URL, params= par)
        json_data = json.loads(response.content)
        new_df = pd.DataFrame(json_data, columns=fields)
        df_prices = pd.concat([df_prices, new_df], axis=0)


        # Move to following period
        initial_timestamp = end_date_timestamp
        end_date_timestamp = initial_timestamp + following_period
        counter+=1

    # End time of function
    loop_end_time = datetime.now()

    time = loop_end_time - loop_start_time
    
    print('DONE'
        , '\nDURATION:', time.days, 'DAYS'
        , time.seconds//3600, 'HOURS', (time.seconds//60)%60, 'MINUTES' 
        , time.seconds%60 , 'SECONDS.')
    print('API CALLS:', counter, ' ROWS:', len(df_prices))


    df_prices = df_prices.rename(columns={'datetime': 'unix_time', 
                                    'open': 'open_price', 
                                    'high': 'high_price',
                                    'low': 'low_price',
                                    'close': 'close_price'})


    df_prices['unix_time'] = df_prices['unix_time'].apply(lambda x: int(round(x / 1000)))

    return df_prices


def get_last_timestamp(base_url,asset_id):

    last_timestamp_response= api_request_last_time_stamp_from_asset_id(base_url,asset_id)

    print("last method"+str(last_timestamp_response))

    last_timestamp = None

    if isinstance(last_timestamp_response, int):
        last_timestamp = last_timestamp_response 
    else:
        if last_timestamp_response["error message"].iloc[0]=="There are not prices for this asset":
            print("There are not prices for this asset")
            last_timestamp = 1638230400 # 30 of november 2021

        elif last_timestamp_response["error message"].iloc[0]=="The Asset with the given id was not found":
            print("The Asset with the given id was not found")
            last_timestamp =None

    return last_timestamp
    
def upload_prices(df_prices,base_url,asset_id):

    if df_prices.empty:
        print("There are NO prices to upload")
    else:
        print("There are prices to upload")
        # loop through all rows and convert each row to a JSON object
        for index, row in df_prices.iterrows():
            
            row_dict = row.to_dict()
            resp = create_price_to_asset_id(base_url,asset_id,row_dict)

    print("DONE upload_prices")
