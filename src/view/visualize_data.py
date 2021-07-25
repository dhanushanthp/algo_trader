import talib
from src.strategies.candle_stick import CandleStick
from src.model_training.prediction import Prediction
import collections


class Visualize:
    def __init__(self):
        # TODO add list of patterns for object reference
        # Provide list of candle stick patterns as list of strings

        self.prediction = Prediction()

        self.cdl_patterns = talib.get_function_groups()['Pattern Recognition']

        # self.cdl_patterns = ['CDLDOJI', 'CDLLONGLEGGEDDOJI', 'CDLENGULFING', 'CDLHARAMI', 'CDL3OUTSIDE',
        #                      'CDLHAMMER', 'CDLHARAMICROSS', 'CDLDRAGONFLYDOJI', 'CDLDOJISTAR',
        #                      'CDLGRAVESTONEDOJI', 'CDLMATCHINGLOW', 'CDL3INSIDE', 'CDLINVERTEDHAMMER', 'CDLSHOOTINGSTAR',
        #                      'CDLMORNINGSTAR', 'CDLEVENINGSTAR', 'CDL3LINESTRIKE', 'CDLMORNINGDOJISTAR', 'CDLEVENINGDOJISTAR',
        #                      'CDLPIERCING', 'CDLTRISTAR', 'CDL3WHITESOLDIERS', 'CDLIDENTICAL3CROWS', 'CDLRISEFALL3METHODS',
        #                      'CDL2CROWS', 'CDL3BLACKCROWS']

        """
        'CDLBELTHOLD', 'CDLLONGLINE', 'CDLHIKKAKE', 'CDLHIKKAKEMOD'
        """

        self.cld_obj = CandleStick(self.cdl_patterns)

    @staticmethod
    def tag_direction(direction):
        """
        Some candle pattern contains the direction of the move. This will capture the direction based on the onehot encode values
        :param direction:
        :return:
        """
        if direction > 0:
            return ' +'
        elif direction < 0:
            return ' -'
        else:
            return ''

    @staticmethod
    def direction_prob(directions: list):
        """
        Find the direction of the next candle based on current candle patterns and suggested directions
        :param directions:
        :return:
        """
        #  Push the list to collections
        counter = collections.Counter(directions)
        # Get the total count
        total_patterns = sum(counter.values())
        # Direction with high count and Direction
        direction, count = counter.most_common(1)[0]

        # Generate string output to show -> Direction, Candle ratio, and winning probability
        return f'[{direction}, {count}/{total_patterns}, {round((count / total_patterns) * 100)}%]'

    def get_candles_visual_data(self, data):
        """
        Generate dat to visualize in UI. This will generate data and Visual annotations

        :param data: candle bar data
        :return: dictionary of data and annotation
        """
        data['merged'] = data.apply(lambda x: [x['open'], x['high'], x['low'], x['close']], axis=1)
        visual_data = list(zip(data['date_epoch'], data['merged']))

        # TODO Add EMA along with candle https://apexcharts.com/javascript-chart-demos/candlestick-charts/candlestick-with-line/
        # chart_data = [{'name': 'candle', 'type': 'candlestick', 'data': visual_data}]

        # Identify patterns
        data = self.cld_obj.generate_pattern(data)
        # Selected columns
        candles = data[['date_epoch'] + self.cdl_patterns]

        # Move the columns to rows
        candles = candles.melt(id_vars=['date_epoch'],
                               var_name="cdl_pattern",
                               value_name="pattern_check")

        # Rename the candle pattens
        candles['cdl_pattern'] = candles['cdl_pattern'].apply(lambda x: x.replace('CDL', ''))
        # Convert as bool values, pick only timeframe with patterns
        candles = candles[candles['pattern_check'].astype(bool)]

        # Add direction of the candle,
        candles['direction'] = candles['pattern_check'].apply(lambda x: self.tag_direction(x))
        candles['cdl_pattern'] = candles['cdl_pattern'] + candles['direction']

        # Combine by time to check multiple intersections
        candles_agg = candles.groupby(['date_epoch'])['cdl_pattern'].agg(list).reset_index()

        # Convert list as String
        candles_agg['cdl_pattern'] = candles_agg['cdl_pattern'].apply(lambda x: ' | '.join(x))

        # Generate direction probability
        direction_agg = candles.groupby(['date_epoch'])['direction'].agg(list).reset_index()
        # Number of candles
        direction_agg['cdl_count'] = direction_agg['direction'].apply(lambda x: len(x))
        direction_agg['direction'] = direction_agg['direction'].apply(lambda x: self.direction_prob(x))

        # Merge candles with the direction probability
        candles_agg = candles_agg.merge(direction_agg, on='date_epoch')

        """
        ALGORITHM
        - Count the total number of patterns for a candle
        - Keep the candle which has more than 3 patterns ( Higher the patterns higher the confirmation)
        - Filter by winning chance of 50% ( TODO May be later)
        """
        # Candle more than 3
        candles_agg = candles_agg[candles_agg['cdl_count'] >= 3].copy()
        candles_agg.drop(['cdl_count'], axis=1, inplace=True)

        # Prepare the annotation list of dictionary into "apexcharts" acceptable format
        annotations = []
        for element in candles_agg.values:
            # annotations.append({'x': int(element[0]), 'label': {'text': f'{element[1]} {element[2]}'}})
            annotations.append({'x': int(element[0]),
                                'label': {'text': f'{element[2]}',
                                          'style': {'fontSize': '15px',
                                                    'background': '#fff',
                                                    'color': '#777'}}})

        return {'data': visual_data, 'annotations': annotations}

    def get_prediction_visual_data(self, data):
        # Generate visual to show candle values
        data['merged'] = data.apply(lambda x: [x['open'], x['high'], x['low'], x['close']], axis=1)
        visual_data = list(zip(data['date_epoch'], data['merged']))

        # Generate candle patterns
        data_patterns = self.cld_obj.generate_pattern(data)

        # Select only candle information
        input_data = data_patterns[self.cdl_patterns]

        # Predict values
        prediction = self.prediction.predict_direction(input_data)

        return prediction
        # Based on prediction generate candle annotations
