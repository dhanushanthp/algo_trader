import time
from tqdm import tqdm
import pandas as pd
from config import Config


class Simulator:
    def __init__(self):
        self.config = Config()

    def write_file_n_min_interval(self, date):
        data = pd.read_csv(f'data/STK/1_min/TSLA/{date}.csv')
        data.index = pd.to_datetime(data['date'])

        # Filter by trading hours, Since my focus is for till 12 AM and most volatile time
        data = data.between_time(self.config.get_filter_time_range()['start'],
                                 self.config.get_filter_time_range()['end']).copy().reset_index(drop=True)

        lines = [','.join(list(str(x) for x in i)) for i in data.values]

        pre_lines = '\n'.join((lines[1:15]))
        with open('realtime_data/data.csv', 'w') as file:
            file.write(''.join(pre_lines) + '\n')

        # Skip the header
        for line in tqdm(lines[15:]):
            time.sleep(60)
            with open('realtime_data/data.csv', 'a') as file:
                file.write(line + '\n')
            time.sleep(60)


if __name__ == '__main__':
    simulator = Simulator()
    simulator.write_file_n_min_interval('20210723')
