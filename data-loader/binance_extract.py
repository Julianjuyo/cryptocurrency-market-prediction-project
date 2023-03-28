#Binance Data Loader

# Import used libraries
import pandas as pd
import datetime as dt
import requests
import json
import csv


test_var = "I am here!"

# Auxiliar Function
def get_last_datetime(filename:str)-> dt.datetime:
    """ This function gets the last time stored in a given file
        in order to start loading data from this point onwards.
    """
    # set file path
    name = filename
    with open(name, "r") as f:
        last_line = f.readlines()[-1]
        
    last_timestamp = int(last_line.split(',')[0])
    last_timestamp//=1000
    print(last_timestamp)
    return dt.datetime.fromtimestamp(last_timestamp)


"""
HOUR

"""

def load_full_data_overwrite_hour(
        filename:str
        , symbol:str = 'BTCUSDT'
        , initial_date:dt.datetime = dt.datetime(2022,9,1)
        , limit_date:dt.datetime = dt.datetime.now() ): 

    """ This function overwrites the whole CSV file with new data.
        
    """

    # Set working dates ------------------------------------------------------------------------------------
    # End of Looping Period Date
    # We will work with time intervals of 16 hours when working with minutes to have 960 records per API call - LIMIT = 1000
    # Load will go from initial_date to limit_date
    # Start date is inclusive
    end_date        = initial_date + dt.timedelta(days=30)# Exclusive

    # Start time of function
    loop_start_time = dt.datetime.now()
    
    # set file path
    name = filename

    #set fields
    fields = ['datetime', 'open', 'high'
    , 'low', 'close', 'volume','close_time'
    , 'qav', 'num_trades','taker_base_vol'
    , 'taker_quote_vol', 'ignore']

    url = 'https://api.binance.com/api/v3/klines'

    counter = 0 
    
    with open(name, 'w') as f:
        # using csv.writer method from CSV package
        write = csv.writer(f)

        write.writerow(fields)

        # Loop through API calls ---------------------------------------------------------------------------
        while initial_date < limit_date:
            # Set dates to Binance API format
            start = str(int(initial_date.timestamp()*1000))

            if end_date > limit_date:
                end = str(int(limit_date.timestamp()*1000))
            else :
                end = str(int(end_date.timestamp()*1000))
            par = {'symbol': symbol, 'interval': '1h', 'startTime': start, 'endTime': end, 'limit':720}
            
            # API CALL
            rows = json.loads(requests.get(url, params= par).text)
            write.writerows(rows)

            # Move to following period
            initial_date = end_date
            end_date = initial_date + dt.timedelta(days=30)
            counter+=1
            
        f.close()
    
    # End time of function
    loop_end_time = dt.datetime.now()

    time = loop_end_time - loop_start_time
    print('DONE'
    
        , '\nDURATION:', time.days, 'DAYS'
        , time.seconds//3600, 'HOURS', (time.seconds//60)%60, 'MINUTES' 
        , time.seconds%60 , 'SECONDS.')
    print('API CALLS:', counter, ' ROWS:', counter * 720)

def update_data_hour (
        filename:str
        , symbol:str = 'BTCUSDT'
        , limit_date:dt.datetime = dt.datetime.now() ): 

    """ 
    """

    initial_date = get_last_datetime(filename)
    
    # Set working dates ------------------------------------------------------------------------------------
    # End of Looping Period Date
    # We will work with time intervals of 16 hours when working with minutes to have 960 records per API call - LIMIT = 1000
    # Load will go from initial_date to limit_date
    # Start date is inclusive
    initial_date = get_last_datetime(filename) + dt.timedelta(hours = 1)
    end_date        = initial_date + dt.timedelta(days=30)# Exclusive

    # Start time of function
    loop_start_time = dt.datetime.now()
    
    # set file path
    name =  filename

    url = 'https://api.binance.com/api/v3/klines'
    counter = 0 
    with open(name, 'a') as f:
        # using csv.writer method from CSV package
        write = csv.writer(f)
        
        # Loop through API calls ---------------------------------------------------------------------------
        while initial_date < limit_date:
            # Set dates to Binance API format
            start = str(int(initial_date.timestamp()*1000))
            end = str(int(end_date.timestamp()*1000))
            par = {'symbol': symbol, 'interval': '1h', 'startTime': start, 'endTime': end, 'limit':720}
            
            # API CALL
            rows = json.loads(requests.get(url, params= par).text)
            write.writerows(rows)

            # Move to following period
            initial_date = end_date
            end_date = initial_date + dt.timedelta(days=30)
            counter+=1
            
        f.close()
    
    # End time of function
    loop_end_time = dt.datetime.now()

    time = loop_end_time - loop_start_time
    print('DONE'
    
        , '\nDURATION:', time.days, 'DAYS'
        , time.seconds//3600, 'HOURS', (time.seconds//60)%60, 'MINUTES' 
        , time.seconds%60 , 'SECONDS.')
    print('API CALLS:', counter, ' ROWS:', counter * 720)
    
    
    
    
    
    
"""
MINUTE

"""

def load_full_data_overwrite_minute(
        filename:str
        , symbol:str = 'BTCUSDT'
        , initial_date:dt.datetime = dt.datetime(2022,9,1)
        , limit_date:dt.datetime = dt.datetime.now() ): 

    # Set working dates ------------------------------------------------------------------------------------
    # End of Looping Period Date
    # We will work with time intervals of 16 hours when working with minutes to have 960 records per API call - LIMIT = 1000
    # Load will go from initial_date to limit_date
    # Start date is inclusive
    end_date        = initial_date + dt.timedelta(hours=16)# Exclusive

    # Start time of function
    loop_start_time = dt.datetime.now()
    
    # set file path
    name = filename

    #set fields
    fields = ['datetime', 'open', 'high'
    , 'low', 'close', 'volume','close_time'
    , 'qav', 'num_trades','taker_base_vol'
    , 'taker_quote_vol', 'ignore']

    url = 'https://api.binance.com/api/v3/klines'

    counter = 0 
    with open(name, 'w') as f:
        # using csv.writer method from CSV package
        write = csv.writer(f)

        write.writerow(fields)

        # Loop through API calls ---------------------------------------------------------------------------
        while initial_date < limit_date:
            # Set dates to Binance API format
            start = str(int(initial_date.timestamp()*1000))

            if end_date > limit_date:
                end = str(int(limit_date.timestamp()*1000))
            else :
                end = str(int(end_date.timestamp()*1000))
            par = {'symbol': symbol, 'interval': '1m', 'startTime': start, 'endTime': end, 'limit':960}
            
            # API CALL
            rows = json.loads(requests.get(url, params= par).text)
            write.writerows(rows)

            # Move to following period
            initial_date = end_date
            end_date = initial_date + dt.timedelta(hours=16)
            counter+=1
            
        f.close()
    
    # End time of function
    loop_end_time = dt.datetime.now()

    time = loop_end_time - loop_start_time
    print('DONE'
    
        , '\nDURATION:', time.days, 'DAYS'
        , time.seconds//3600, 'HOURS', (time.seconds//60)%60, 'MINUTES' 
        , time.seconds%60 , 'SECONDS.')
    print('API CALLS:', counter, ' ROWS:', counter * 960)

def update_data_minute(
        filename:str
        , symbol:str = 'BTCUSDT'
        , limit_date:dt.datetime = dt.datetime.now() ): 

    initial_date = get_last_datetime(filename)
    
    # Set working dates ------------------------------------------------------------------------------------
    # End of Looping Period Date
    # We will work with time intervals of 16 hours when working with minutes to have 960 records per API call - LIMIT = 1000
    # Load will go from initial_date to limit_date
    # Start date is inclusive
    initial_date = get_last_datetime(filename) + dt.timedelta(minutes = 1)
    end_date        = initial_date + dt.timedelta(hours=16)# Exclusive

    # Start time of function
    loop_start_time = dt.datetime.now()
    
    # set file path
    name =  filename

    url = 'https://api.binance.com/api/v3/klines'
    counter = 0 
    with open(name, 'a') as f:
        # using csv.writer method from CSV package
        write = csv.writer(f)
        
        # Loop through API calls ---------------------------------------------------------------------------
        while initial_date < limit_date:
            # Set dates to Binance API format
            start = str(int(initial_date.timestamp()*1000))
            end = str(int(end_date.timestamp()*1000))
            par = {'symbol': symbol, 'interval': '1m', 'startTime': start, 'endTime': end, 'limit':960}
            
            # API CALL
            rows = json.loads(requests.get(url, params= par).text)
            write.writerows(rows)

            # Move to following period
            initial_date = end_date
            end_date = initial_date + dt.timedelta(hours=16)
            counter+=1
            
        f.close()
    
    # End time of function
    loop_end_time = dt.datetime.now()

    time = loop_end_time - loop_start_time
    print('DONE'
    
        , '\nDURATION:', time.days, 'DAYS'
        , time.seconds//3600, 'HOURS', (time.seconds//60)%60, 'MINUTES' 
        , time.seconds%60 , 'SECONDS.')
    print('API CALLS:', counter, ' ROWS:', counter * 960)