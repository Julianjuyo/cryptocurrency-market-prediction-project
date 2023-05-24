from models.price import Price as PriceModel
from models.asset import Asset as AssetModel
from models.indicator import Indicator as IndicatorModel


from services.utils import * # add_indicators, find_file_and_config_json, round_day, round_minute, round_hour,merge_dataframes,predict
from services.price import PriceService


from schemas.indicator import Indicator
from schemas.indicator import UpdateIndicator

from sqlalchemy.orm import joinedload

from sqlalchemy import and_
from sqlalchemy import desc

from fastapi.encoders import jsonable_encoder

import numpy as np
import pandas as pd
import os
import sys


class PredictService():


    def __init__(self, db) -> None:
        self.db = db



    def get_indicators_and_merge(self, asset_id, unix_time_end, future_time ):


        unix_time_end = int(unix_time_end)

        unix_time_now = int(datetime.now().timestamp())


        if unix_time_end >= unix_time_now:
            print("ETRNOU")
            return {'error message': 'The datetime since you want to predict has to be in the past'}

        asset = self.db.query(AssetModel).filter(
            AssetModel.id == asset_id).first()

        if not asset:
            return {'error message': "The asset with the given id was not found"}
        

        asset_json = jsonable_encoder(asset)

        interval = asset_json["interval"]

        file_path, config_json = find_file_and_config_json(asset_json["symbol"], interval, future_time)

        if not file_path:
            return {'error message': 'There are no models for the given asset and future_time'}

        delay = config_json["delay"]
        sampling_rate = config_json["sampling_rate"]
        sequence_length = config_json["sequence_length"]
        batch_size = config_json["batch_size"]
        # se debe sumar el delay dos veces para tener el tiempo adecuado
        number_data_past= (sequence_length * sampling_rate) + (delay*2)

        if interval == "minute":
            unix_time_end_round = round_minute(unix_time_end)
            unix_time_start = unix_time_end_round - ((number_data_past) * 60)
            first_indicator_time = unix_time_start - 6000
            increment = 60

        if interval == "hour":
            unix_time_end_round = round_hour(unix_time_end)
            unix_time_start = unix_time_end_round - ((number_data_past) * 3600)
            first_indicator_time = unix_time_start - 360000
            increment = 3600

        if interval == "day":

            unix_time_end_round = round_day(unix_time_end)
            unix_time_start = unix_time_end_round - ((number_data_past) * 86400)
            first_indicator_time = unix_time_start - 8640000
            increment = 86400


        last_price = self.db.query(PriceModel).filter(PriceModel.asset_id == asset_id).order_by(desc(PriceModel.unix_time)).first()

        if not last_price:
            return {'error message': "There are not prices for this asset"}
        
        last_price_json = jsonable_encoder(last_price)

        last_unix_time = last_price_json["unix_time"]

        if unix_time_end_round > last_unix_time:
            return {'error message': "The selected datetime is bigger than the last price datetime in the database",
                    'timestamp': last_unix_time }
        

        prices = self.db.query(PriceModel).filter(and_(
            PriceModel.unix_time >= first_indicator_time, PriceModel.unix_time <= unix_time_end_round, PriceModel.asset_id == asset_id)).all()

        if not prices:
            return {'error message': 'The are no Prices with the given unix_time range'}
        
        prices_json = jsonable_encoder(prices)

        df = pd.json_normalize(prices_json)

        df['close_time'] = df['unix_time'] + (increment - 1)

        df_prices_wit_indicators_all = add_indicators(df)

        df_prices_wit_indicators = df_prices_wit_indicators_all.loc[df_prices_wit_indicators_all['unix_time'] > unix_time_start]


        print("numero data: "+str(number_data_past))
        print("numero dataframe final: "+ str(len(df_prices_wit_indicators)))
        print("unix_time_end: "+str(unix_time_end))
        print("unix_time_start: "+ str(unix_time_start))
        print("unix_time_end_round: "+ str(unix_time_end_round))
        print("first_indicator_time: "+ str(first_indicator_time))
              
        



        # Sort the dataframe by 'unix_time' column in ascending order
        df_sorted = df_prices_wit_indicators.sort_values('unix_time', ascending=True)


        predicted_prices = predict(df_sorted, file_path,delay,sampling_rate,sequence_length, batch_size)


        # Select only data necesary
        df_initial = df_prices_wit_indicators[["unix_time", "open_price", "close_price", "low_price", "high_price", "volume"]].copy()

        df_initial = df_initial.loc[df_initial['unix_time'] >= (df_initial['unix_time'].max()-(increment*50))]

        return merge_dataframes(predicted_prices,df_initial,increment)





        


