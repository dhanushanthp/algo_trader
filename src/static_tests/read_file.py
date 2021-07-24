import pandas as pd
import json
import talib
from src.strategies.candle_stick import CandleStick
from src.view.visualize_data import Visualize
from src.utils.data_util import DataUtil


class FileRead:
    def __init__(self):
        self.visual_ref = Visualize()
        self.data_util_ref = DataUtil()

    def get_data(self, day):
        # This provide the previous day night and current day mid morning day

        df = pd.read_csv(f'data/STK/1_min/TSLA/{day}.csv')

        df = self.data_util_ref.pre_data_process(df)

        output = self.visual_ref.get_candles_visual_data(df)

        return json.dumps([output['data'][-30:], output['annotations']])


