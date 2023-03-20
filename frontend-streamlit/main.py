import streamlit as st
import requests
import pandas as pd
import os
import time
import json


ON_DOCKER = os.environ.get('ON_DOCKER', False)

st.set_page_config(layout='wide')


"""
# Artificial Intelligence Techniques Applied to Cryptocurrency Market Prediction

## Authors:

* Juan Diego Sanchez
* Julian Oliveros Forero

"""


# Buscar la lista de exchanges que se quieren seleccionar

if ON_DOCKER:
    base_url = "http://fastapi:5000/"
else:
    base_url = "http://0.0.0.0:5000/"


filelist = [" "]


# Make the api reuqest to get all the exchanges
def api_request_get_all_exchanges(base_url):

    try:

        response = requests.get(base_url+"exchanges")
        json_data = json.loads(response.content)
        df = pd.json_normalize(json_data)
        return df
    except:
        st.error("Error while make the http Request")

    

# Make the api request to get all tha Assets from a exchnage


def api_request_get_all_assets_from_exchange_id(base_url, exchange_id):

    try:
        response = requests.get(base_url+"exchange/"+exchange_id+"/asset")
        json_data = json.loads(response.content)
        df = pd.json_normalize(json_data)
    except:
        st.error("Error while make the http Request")
    return df


def api_request_predicts_from_asset_id(base_url, asset_id):

    try:
        response = requests.get(base_url+"predicts/"+asset_id)
        json_data = json.loads(response.content)
        df = pd.json_normalize(json_data)
    except:
        st.error("Error while make the http Request")
    return df


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

        # Get the number of minutes in the future it wants to predict
        number_minutes = st.number_input(
            "Indicate the number of minutes you want to predict in the future", min_value=0, value=0)

        submit_selected_file = st.button("Predict")

        if submit_selected_file and number_minutes > 0:

            st.write("Asset to predict: ", asset_symbol,
                     " with an interval of ", asset_interval)

            # request to the backend to get the prediction
            with st.spinner('Please wait while the algorithm is predicting...'):

                time.sleep(1)

                resp = api_request_predicts_from_asset_id(
                    base_url, selected_asset)

            # Show the output of the prediccion
            st.success("The value is of the price is: " +
                       str(resp["close_price"].iloc[0]))

        if submit_selected_file and number_minutes < 1:

            st.error("The number of minutes have to be greated than 0")


if __name__ == "__main__":
    pass
