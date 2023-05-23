import streamlit as st
import requests
import pandas as pd
import os
import time
import json
from datetime import datetime, timedelta


# Bokeh imports for the candlestick chart
import bokeh
from math import pi
from bokeh.plotting import figure
from bokeh.io import output_notebook,show
from bokeh.resources import INLINE
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, DatetimeTickFormatter


ON_DOCKER = os.environ.get('ON_DOCKER', False)

st.set_page_config(layout='wide')


"""
# Artificial Intelligence Techniques Applied to Cryptocurrency Market Prediction

## Authors:

* Juan Diego Sanchez
* Julian Oliveros Forero

### The objective of this project is to enhance comprehension of market predictability by employing machine learning techniques. This endeavor aims to assist cryptocurrency investors and stakeholders in making informed decisions by predicting market prices and trends, focusing specifically on Bitcoin, Ethereum, and Cardano. Machine learning models will be trained using historical market data to achieve this goal.

"""


# Check if the app is running on docker
if ON_DOCKER:
    base_url = "http://fastapi:5000/"
else:
    base_url = "http://0.0.0.0:5000/"


# Create a candlestick chart for the selected exchange and asset
def candlestick_chart(df, interval, title_name):


    df["datetime"] = pd.to_datetime(df["datetime"])

    st.write(df)

    st.write("The line_color blue is the future data")

    # Set the index of the dataframe to the 'date' column
    df = df.set_index('datetime')

    # Define variables for increasing and decreasing prices
    

    inc_new = (df.close_price > df.open_price) & (df.volume <= 0)
    dec_new = (df.open_price > df.close_price) & (df.volume <= 0)

    inc = (df.close_price > df.open_price) & (df.volume > 0)
    dec = (df.open_price > df.close_price) & (df.volume > 0)


    # Set the width of the bars based on the interval
    if interval == "minute":
        w = 12*1000 
    if interval =="hour":
        w = 12*60*1000 
    if interval =="day":
        w = 12*60*60*1000 

    ## Candlestick chart
    # Create a figure for the candlestick chart with a datetime x-axis and a title
    candlestick = figure(x_axis_type="datetime", title = str(title_name+" in "+interval+ " Interval"))


    # Plot the high and low prices as line segments
    candlestick.segment(df.index, df.high_price, df.index, df.low_price, color="black")

    

    # # Plot the increasing prices as red bars and the decreasing prices as green bars
    candlestick.vbar(df.index[inc_new], w, df.open_price[inc_new], df.close_price[inc_new],
            fill_color="red", line_color="blue")

    candlestick.vbar(df.index[dec_new], w, df.open_price[dec_new], df.close_price[dec_new],
            fill_color="green", line_color="blue")
    
    candlestick.vbar(df.index[inc], w, df.open_price[inc], df.close_price[inc],
            fill_color="red", line_color="red")

    candlestick.vbar(df.index[dec], w, df.open_price[dec], df.close_price[dec],
            fill_color="green", line_color="green")
    
   
    

    ## Volume Chart
    # Create a figure for the volume chart with a datetime x-axis
    volume = figure(x_axis_type="datetime")

    # Plot the volume as bars with a specified width and color
    volume.vbar(df.index, width=w, top=df.volume,
                fill_color="dodgerblue", line_color="dodgerblue", alpha=0.8)

    # Set the font size and alignment of the title
    candlestick.title.text_font_size = "20pt"
    candlestick.title.align = "center"

    # Set the y-axis labels for both charts
    volume.yaxis.axis_label="Volume"
    candlestick.yaxis.axis_label="Price ($)"

    # Set the x-axis label for the volume chart with the interval specified
    volume.xaxis.axis_label="Date in "+interval

    # Combine the two charts into a column layout and return it
    return column(candlestick), column(volume)


# Buscar la lista de exchanges que se quieren seleccionar
filelist = [" "]

# Dict with future values
future_times ={
    "ADAUSDT":{
        "minute": ["1h", "3h", "6h", "12h", "24h","3d", "7d"],
        "hour"  : ["1h", "3h", "6h", "12h", "24h","3d", "7d"]
    },
    "ETHUSDT":{
        "minute": ["1h", "3h", "6h", "12h", "24h","3d", "7d"],
        "hour"  : ["1h", "3h", "6h", "12h", "24h","3d", "7d"]
    },
    "BTCUSDT":{
        "minute": ["1h", "3h", "6h", "12h", "24h","3d", "7d"],
        "hour"  : ["1h", "3h", "6h", "12h", "24h","3d", "7d"]
    } 
}

# Make the api request to get all the exchanges
def api_request_get_all_exchanges(base_url):

    try:

        response = requests.get(base_url+"exchanges/")
        json_data = json.loads(response.content)
        df = pd.json_normalize(json_data)
        return df
    except:
        st.error("Error while make the http Request")

    

# Make the api request to get all tha Assets from a exchnage

def api_request_get_all_assets_from_exchange_id(base_url, exchange_id):

    try:
        print(base_url)
        response = requests.get(base_url+"exchanges/"+exchange_id+"/asset/")
        print(response)
        json_data = json.loads(response.content)
        df = pd.json_normalize(json_data)
    except:
        st.error("Error while make the http Request")
    return df



# to get the prediction for a specific asset
def api_request_predicts_from_asset_id(base_url, asset_id,future_time):

    try:
        response = requests.get(base_url+"predicts/"+asset_id+"/future_time/"+future_time)
        json_data = json.loads(response.content)
        df = pd.json_normalize(json_data)
    except:
        st.error("Error while make the http Request")
    return df

# Get the unix times for the selected interval
def get_unix_times(interval):

    # Get current timestamp
    current_time = datetime.now()
    if interval == "minute":
        time_delta = timedelta(minutes=300)
    if interval == "hour":
        time_delta = timedelta(hours=240)
    if interval == "day":
        time_delta = timedelta(days=10)

    time_past = current_time - time_delta

    return int(time_past.timestamp()), int(current_time.timestamp())


# Convert unix time to datetime
def convert_unix_time(unix_time):
    utc_datetime = datetime.utcfromtimestamp(unix_time)
    return utc_datetime


# Get all the Exchanges
exchange=""
try:
    exchanges_api = api_request_get_all_exchanges(base_url)
    exchanges_api = pd.DataFrame(
        [[" ", " ", " ", " "]], columns=exchanges_api.columns).append(exchanges_api)

    st.header("Select The Asset you want to predict")
    exchange = st.selectbox("Select the Exchange", exchanges_api["name"])

except:
    st.error("Error while make the http Request")


if len(exchange) > 1:

    # Get the id of the selected_asset
    selected_exchange_id = exchanges_api.loc[exchanges_api['name']
                                             == exchange, "id"].iloc[0]

    selected_asset = " "

    try:
        # Get all the assets from that exchange

        assets_api = api_request_get_all_assets_from_exchange_id(
            base_url, selected_exchange_id)
        
        
        assets_api = pd.DataFrame(
            [[" ", " ", " ", " ", " ", " ", " ", " ", " "]], columns=assets_api.columns).append(assets_api)


        # Get the symbol of the asset
        asset_symbol = st.selectbox("Select the Asset", assets_api["symbol"].unique())
        selected_symbol = assets_api.loc[assets_api['symbol']
                                         == asset_symbol, "interval"]

        # Get the interval of the asset
        asset_interval = st.selectbox(
            "Select the Asset interval time", selected_symbol)

        # Get the id of the asset
        selected_asset = assets_api.loc[(assets_api['symbol'] == asset_symbol) & (
            assets_api['interval'] == asset_interval), "id"].iloc[0]

    except:
        st.error("Theres no Assets for this exchange")

    if len(selected_asset) > 1:

        future_time = None
        # Get the number of minutes in the future it wants to predict
        future_time = st.selectbox(
            "Indicate the number of "+ asset_interval+" you want to predict in the future",future_times[asset_symbol][asset_interval])

        submit_selected_file = st.button("Predict")

        if submit_selected_file and future_time != None:

            st.write("Asset to predict: ", asset_symbol,
                     " with an interval of ", asset_interval)

            # request to the backend to get the prediction
            with st.spinner('Please wait while the algorithm is predicting...'):

                time.sleep(1)

                resp = api_request_predicts_from_asset_id(
                    base_url, selected_asset, future_time)


            # Show the output of the prediccion
            st.success("The value is of the price is: " +
                       str( resp.loc[(resp['unix_time'] == resp['unix_time'].max()), "close_price"].iloc[0]))
            


            # #bring the past prices  to show the graph
            # prices = api_request_get_prices_between_unix_time(base_url,selected_asset,get_unix_times(asset_interval)[0], get_unix_times(asset_interval)[1])

    
            resp['datetime'] = resp['unix_time'].apply(convert_unix_time)

            # Show the graph of the prediction
            chart = candlestick_chart(resp, asset_interval,asset_symbol)

            st.bokeh_chart(chart[0],use_container_width=True)     
            st.bokeh_chart(chart[1],use_container_width=True)   

           


        if submit_selected_file and future_time == None:

            st.error("Theres not future time selected")


if __name__ == "__main__":
    pass
