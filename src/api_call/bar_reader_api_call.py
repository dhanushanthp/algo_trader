from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.wrapper import BarData
from ibapi.contract import Contract
from ibapi.client import TickAttribLast, TickerId, TickAttribBidAsk
import sys
import os
import datetime


class IBapi(EWrapper, EClient):
    def __init__(self, ticker):
        """
        We will be collecting realtime bar data (open, close, high, low) every 5 seconds based on IB API heartbeat. The data from API will be passed
        to function for further analysis.

        https://interactivebrokers.github.io/tws-api/historical_bars.html#hd_request

        :param ticker:
        """
        EClient.__init__(self, self)
        self.previous_ts = None
        # Collect 1 min of data with 5 sec frequency
        self.data_collection = list()

    def error(self, reqId: TickerId, errorCode: int, errorString: str):
        print(f"{reqId}, {errorCode}, {errorString}")

    def historicalData(self, reqId: int, bar: BarData):
        """
        Pull all historic data for the specific data
        :param reqId:
        :param bar:
        :return:
        """
        with open('realtime_data/data.csv', 'a') as file:
            file.write(f'{bar.date},{bar.open},{bar.high},{bar.low},{bar.close},{bar.barCount},{bar.volume},{bar.average}\n')

    def historicalDataUpdate(self, reqId: int, bar: BarData):
        # With the 5sec refresh, this will be one of the filter to avoid overloaded responses through the process
        # Sometimes the bar count is -2147483536, that created duplicated timestamp
        if (bar.volume > 0) and (bar.barCount > 0):
            # When the time the API call on exact time the machine seconds will be 0. The data will be push to file on exact time
            if datetime.datetime.now().second == 0:
                print(bar.date)

                with open('realtime_data/data.csv', 'a') as file:
                    file.write(f'{bar.date},{bar.open},{bar.high},{bar.low},'
                               f'{bar.close},{bar.barCount},{bar.volume},{bar.average}\n')


def main():
    ticker = str(sys.argv[1]).upper()
    app = IBapi(ticker)
    # config = Config()
    app.connect(host='127.0.0.1', port=7497, clientId=19878)

    # Create contract object
    contract = Contract()
    contract.symbol = ticker
    contract.secType = 'STK'
    contract.exchange = 'SMART'
    contract.currency = 'USD'
    contract.primaryExchange = 'NASDAQ'

    # Remove realtime data file
    os.remove('realtime_data/data.csv')

    # Request historical candles
    app.reqHistoricalData(1009, contract, "", "1 D", "1 min", "TRADES", 0, 1, True, [])
    app.run()


main()
