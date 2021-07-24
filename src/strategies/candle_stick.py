import talib
import pandas_ta


class CandleStick:
    def __init__(self, cdl_pattern_list: list):
        self.chart_patterns = cdl_pattern_list

    def generate_pattern(self, data):
        """
        Generate candle stick patterns for given data frame. The patterns will be generated based on the given input.
        e.g. The input data could be in various time frames such as 1min, 2 min or 5 min. As long as the pattern match. it will generate a
        value inside of dataframe
        :param data: Bar data from stocks
        :return: Pattern added data set. The new column with "CDL" name
        """

        for pattern in self.chart_patterns:
            # Call the function by name
            fun_candle_pattern = getattr(talib, pattern)

            data[pattern] = fun_candle_pattern(data['open'], data['high'], data['low'], data['close'])

        # Generate EMAs
        data['9EMA'] = pandas_ta.ema(data['close'], length=9)
        data['20EMA'] = pandas_ta.ema(data['close'], length=20)

        return data


