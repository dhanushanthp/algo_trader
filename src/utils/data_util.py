import pandas as pd
import json
import talib
from src.strategies.candle_stick import CandleStick
from src.view.visualize_data import Visualize
from config import Config


class DataUtil:
    def __init__(self):
        self.visual_ref = Visualize()
        self.config = Config()

    def pre_data_process(self, data):
        """
        This function will filter the data by 930 to 12

        :param data:
        :return:
        """
        # This provide the previous day night and current day mid morning day
        data['date'] = pd.to_datetime(data['date'])
        # Index date time for filtering purpose
        data.index = data['date']

        # Filter by trading hours, Since my focus is for till 12 AM and most volatile time
        data = data.between_time(self.config.get_filter_time_range()['start'], self.config.get_filter_time_range()['end']).copy()

        # Reset Index
        data.reset_index(drop=True, inplace=True)

        # Create time entry
        data['time'] = data['date'].dt.time
        # Date String
        data['date_str'] = data['date'].dt.date.apply(lambda x: x.strftime('%Y-%m-%d'))

        # Conversion as epoch
        data['date_epoch'] = data['date'].apply(lambda x: int(x.timestamp()) + (3600 * 4))

        return data
