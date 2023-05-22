
from datetime import datetime, timezone

import pytz
import ta
import os
import sys
import json



# imports for the models
import numpy as np
import pandas as pd
import math

# import tensorflow as tf
# from tensorflow import keras
# from tensorflow.keras.utils import Sequence
# from sklearn.preprocessing import MinMaxScaler
# from sklearn.metrics import mean_squared_error
# from tensorflow.keras.models import load_model



def convert_unix_time(unix_time):
    utc_datetime = datetime.utcfromtimestamp(unix_time)
    gmt5_tz = pytz.timezone("America/Bogota")
    gmt5_datetime = utc_datetime.astimezone(gmt5_tz)
    return utc_datetime, gmt5_datetime


def find_file_and_config_json(symbol, interval, future_time):
    # sys.path.append('/ml-models/')

    try:

        filename = f"{symbol}_{interval}_{future_time}_ahead.h5"

        directory = os.getcwd()+"/ml-models/"+symbol+"/"+interval+"/"
        path = None
        for root, dirs, files in os.walk(directory):

            if filename in files:
                path = os.path.join(root, filename)

        # Open the file and load its contents
        with open(str(directory+"config.json")) as file:
            data = json.load(file)

        return path, data[filename]
    
    except:
        return None, None


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


# def data_preparation(df):

#     # drop the datetime column
#     df_reduced = df.drop(columns=['datetime'])

#     scaler = MinMaxScaler()

#     # Fit the scaler on your dataframe (let's say it's called df)
#     df_normalized = scaler.fit_transform(df_reduced)

#     # Convert the normalized data back to a dataframe
#     df_normalized = pd.DataFrame(df_normalized, columns=df_reduced.columns)

#     # Convert the DataFrame to a NumPy array
#     raw_data = df_normalized.values
#     close = df_normalized['close_price'].values
#     close = close.reshape((len(close),1))

#     # Display the NumPy array
#     print(type(raw_data))
#     print(raw_data.shape)
#     print(close.shape)

#     return raw_data, close



# def predict(df,model_path,delay,sampling_rate,sequence_length):

#     raw_data, close = data_preparation(df)

#     # Set Parameters

#     # sequence_stride: period between sequences
#     # First sequence starts at t0
#     # Second sequence will start at t1 with sequence_stride=1 or at t5 with sequence_stride=5
#     sequence_stride = 1

#     #batch_size: Number of timeseries samples in each batch (except maybe the last one). 
#     #If None, the data will not be batched (the dataset will yield individual samples).
#     # Huge impact in performance.
#     # Tip, should be multiple of 8
#     batch_size = 32

#     # Understanding our parameters
#     msg = f"The timeseries will consist of batches containing {batch_size} sequences of {sequence_length} samples."

#     msg += f"\nFinally our target is {delay} timesteps in the future, and will have data from {sequence_length * sampling_rate} timesteps in the past"
#     print(msg)

#     keras_dataset = keras.preprocessing.timeseries_dataset_from_array(
#                         raw_data[:-delay],
#                         targets=close[delay:],
#                         sampling_rate=sampling_rate,
#                         sequence_stride=sequence_stride,
#                         sequence_length=sequence_length,
#                         shuffle=False, # Shouldn't the shuffle be set to 0?
#                         seed=33,
#                         batch_size=batch_size,
#                         start_index=0)
    
#     # Load the model from the .h5 file
#     modelo =  load_model(model_path)

#     test_pred = modelo.predict(keras_dataset)

#     # Assume 'y_normalized' contains the predicted values for the 'target' column in normalized form
#     y_min = df['close_price'].min()
#     y_max = df['close_price'].max()

#     test_pred = test_pred * (y_max - y_min) + y_min

#     predicted_prices = pd.DataFrame(test_pred, columns=['close_price'])

#     return predicted_prices


# Function to add incremental number starting from a specific value
def add_incremental_number(row, increment, starting_number):
    return starting_number + row.name * increment


def merge_dataframes(predicted_prices, df_initial,increment):

    print(df_initial.columns)

    print(df_initial['unix_time'].max())

    starting_number = df_initial['unix_time'].max()+increment

    last_close_price = df_initial.loc[(df_initial['unix_time'] == df_initial['unix_time'].max()), "close_price"].iloc[0]

    predicted_prices['unix_time'] = predicted_prices.apply(add_incremental_number, args=(increment, starting_number), axis=1)

    # insert the last close price as the open price of the first row
    predicted_prices['open_price'] = predicted_prices['close_price'].shift(1)


    # Find the index of the row with the specified unix_time
    index = predicted_prices.loc[predicted_prices['unix_time'] == starting_number].index[0]

    # Replace the open_price value of the specified row with 20
    predicted_prices.at[index, 'open_price'] = last_close_price

    # craete a new column with 0 values for the volume
    predicted_prices['volume'] = 0

    # Create the new 'low_price' column with the specified conditions
    predicted_prices['low_price'] = predicted_prices.apply(lambda row: row['close_price'] if row['close_price'] < row['open_price']
                                else row['open_price'], axis=1)


    # Create the new 'high_price' column with the specified conditions
    predicted_prices['high_price'] = predicted_prices.apply(lambda row: row['open_price'] if row['close_price'] < row['open_price']
                                else row['close_price'], axis=1)


    result_df = pd.concat([df_initial, predicted_prices], axis=0)
    result_df.sort_values('unix_time', ascending=True, inplace=True)

    return result_df



# method to add the thecnic indicators to the dataframe
def add_indicators(df):

    # momentum
    df['ao'] = ta.momentum.awesome_oscillator(
        high=df['high_price'], low=df['low_price'])
    df['kama'] = ta.momentum.kama(close=df['close_price'])
    df['ppo'] = ta.momentum.ppo(close=df['close_price'])
    df['pvo'] = ta.momentum.pvo(volume=df['volume'])
    df['roc'] = ta.momentum.roc(close=df['close_price'])
    df['rsi'] = ta.momentum.rsi(close=df['close_price'])
    df['stochrsi'] = ta.momentum.stochrsi(close=df['close_price'])
    df['stoch'] = ta.momentum.stoch(
        close=df['close_price'], high=df['high_price'], low=df['low_price'])
    df['tsi'] = ta.momentum.tsi(close=df['close_price'])
    df['uo'] = ta.momentum.ultimate_oscillator(
        close=df['close_price'], high=df['high_price'], low=df['low_price'])
    df['wri'] = ta.momentum.williams_r(
        close=df['close_price'], high=df['high_price'], low=df['low_price'])

    # volume
    df['accdist'] = ta.volume.acc_dist_index(
        high=df['high_price'], low=df['low_price'], close=df['close_price'], volume=df['volume'])
    df['cmf'] = ta.volume.chaikin_money_flow(
        high=df['high_price'], low=df['low_price'], close=df['close_price'], volume=df['volume'])
    df['emv'] = ta.volume.ease_of_movement(
        high=df['high_price'], low=df['low_price'], volume=df['volume'])
    df['fi'] = ta.volume.force_index(
        close=df['close_price'], volume=df['volume'])
    df['mfi'] = ta.volume.money_flow_index(
        high=df['high_price'], low=df['low_price'], close=df['close_price'], volume=df['volume'])
    df['nvi'] = ta.volume.negative_volume_index(
        close=df['close_price'], volume=df['volume'])
    df['obv'] = ta.volume.on_balance_volume(
        close=df['close_price'], volume=df['volume'])
    df['smaemv'] = ta.volume.sma_ease_of_movement(
        high=df['high_price'], low=df['low_price'], volume=df['volume'])
    df['vpt'] = ta.volume.volume_price_trend(
        close=df['close_price'], volume=df['volume'])
    df['vwap'] = ta.volume.volume_weighted_average_price(
        high=df['high_price'], low=df['low_price'], close=df['close_price'], volume=df['volume'])

    # volatility
    df['atr'] = ta.volatility.average_true_range(
        high=df['high_price'], low=df['low_price'], close=df['close_price'])
    df['ulcer'] = ta.volatility.ulcer_index(close=df['close_price'])

    df['bbh'] = ta.volatility.bollinger_hband(close=df['close_price'])
    df['bbl'] = ta.volatility.bollinger_lband(close=df['close_price'])
    df['bbhi'] = ta.volatility.bollinger_hband_indicator(
        close=df['close_price'])
    df['bbli'] = ta.volatility.bollinger_lband_indicator(
        close=df['close_price'])
    df['bbmavg'] = ta.volatility.bollinger_mavg(close=df['close_price'])
    df['bb_pb'] = ta.volatility.bollinger_pband(close=df['close_price'])
    df['bb_wb'] = ta.volatility.bollinger_wband(close=df['close_price'])

    df['dchb'] = ta.volatility.donchian_channel_hband(
        close=df['close_price'], high=df['high_price'], low=df['low_price'])
    df['dclb'] = ta.volatility.donchian_channel_lband(
        close=df['close_price'], high=df['high_price'], low=df['low_price'])
    df['dcmb'] = ta.volatility.donchian_channel_mband(
        close=df['close_price'], high=df['high_price'], low=df['low_price'])
    df['dcpb'] = ta.volatility.donchian_channel_pband(
        close=df['close_price'], high=df['high_price'], low=df['low_price'])
    df['dcwb'] = ta.volatility.donchian_channel_wband(
        close=df['close_price'], high=df['high_price'], low=df['low_price'])

    df['kchb'] = ta.volatility.keltner_channel_hband(
        close=df['close_price'], high=df['high_price'], low=df['low_price'])
    df['kclb'] = ta.volatility.keltner_channel_lband(
        close=df['close_price'], high=df['high_price'], low=df['low_price'])
    df['kchbi'] = ta.volatility.keltner_channel_hband_indicator(
        close=df['close_price'], high=df['high_price'], low=df['low_price'])
    df['kclbi'] = ta.volatility.keltner_channel_lband_indicator(
        close=df['close_price'], high=df['high_price'], low=df['low_price'])
    df['kcmb'] = ta.volatility.keltner_channel_mband(
        close=df['close_price'], high=df['high_price'], low=df['low_price'])
    df['kcpb'] = ta.volatility.keltner_channel_pband(
        close=df['close_price'], high=df['high_price'], low=df['low_price'])
    df['kcwb'] = ta.volatility.keltner_channel_wband(
        close=df['close_price'], high=df['high_price'], low=df['low_price'])

    # trend

    # En dos de estos tres hay algo que esta botando warning
    # df['adx'] = ta.trend.adx(close=df['close_price'],
    #                          high=df['high_price'], low=df['low_price'])
    # df['adx_neg'] = ta.trend.adx_neg(
    #     close=df['close_price'], high=df['high_price'], low=df['low_price'])
    # df['adx_pos'] = ta.trend.adx_pos(
    #     close=df['close_price'], high=df['high_price'], low=df['low_price'])

    df['aroon_up'] = ta.trend.aroon_up(close=df['close_price'])
    df['aroon_down'] = ta.trend.aroon_down(close=df['close_price'])

    df['cci'] = ta.trend.cci(close=df['close_price'],
                             high=df['high_price'], low=df['low_price'])
    df['dpo'] = ta.trend.dpo(close=df['close_price'])
    df['kst'] = ta.trend.kst(close=df['close_price'])
    df['kst_sig'] = ta.trend.kst_sig(close=df['close_price'])
    df['ema'] = ta.trend.ema_indicator(close=df['close_price'])

    df['ichimoku_a'] = ta.trend.ichimoku_a(
        high=df['high_price'], low=df['low_price'])
    df['ichimoku_b'] = ta.trend.ichimoku_b(
        high=df['high_price'], low=df['low_price'])
    df['ichimoku_base_line'] = ta.trend.ichimoku_base_line(
        high=df['high_price'], low=df['low_price'])
    df['ichimoku_conversion_line'] = ta.trend.ichimoku_conversion_line(
        high=df['high_price'], low=df['low_price'])

    df['macd'] = ta.trend.macd(close=df['close_price'])
    df['macd_diff'] = ta.trend.macd_diff(close=df['close_price'])
    df['macd_signal'] = ta.trend.macd_signal(close=df['close_price'])

    df['mi'] = ta.trend.mass_index(high=df['high_price'], low=df['low_price'])
    df['sma'] = ta.trend.sma_indicator(close=df['close_price'])
    df['wma'] = ta.trend.wma_indicator(close=df['close_price'])
    df['stc'] = ta.trend.stc(close=df['close_price'])
    # df['trix'] = ta.trend.trix(close=df['close_price'])

    df['vi_pos'] = ta.trend.vortex_indicator_pos(
        close=df['close_price'], high=df['high_price'], low=df['low_price'])
    df['vi_neg'] = ta.trend.vortex_indicator_neg(
        close=df['close_price'], high=df['high_price'], low=df['low_price'])

    return df


