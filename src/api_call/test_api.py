from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.wrapper import BarData
import pandas as pd

import threading
import time


class IBapi(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
        self.data = []

    def historicalData(self, reqId: int, bar: BarData):
        """
        Pull all historic data for the specific data
        :param reqId:
        :param bar:
        :return:
        """
        self.data.append([bar.date, bar.open, bar.high, bar.low, bar.close, bar.barCount, bar.volume, bar.average])
        print(bar)


def run_loop():
    app = IBapi()
    app.connect('127.0.0.1', 7497, 123)
    # Create contract object
    apple_contract = Contract()
    apple_contract.symbol = 'AAPL'
    apple_contract.secType = 'STK'
    apple_contract.exchange = 'SMART'
    apple_contract.currency = 'USD'

    # Request Market Data
    app.reqHistoricalData(1009, apple_contract, "", "1800 S", "1 min", "TRADES", 0, 1, True, [])
    time.sleep(3)
    app.run()
    print('hello')
    app.disconnect()


api_thread = threading.Thread(target=run_loop)
api_thread.start()
api_thread.join()

# time.sleep(1)  # Sleep interval to allow time for connection to server

# time.sleep(2)  # Sleep interval to allow time for incoming price data

print('process complete')
