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
        if (bar.volume > 0) and (bar.barCount > 0):
            # if datetime.datetime.now().second == 0:
            #     print(bar.date)
            #
            #     with open('realtime_data/data.csv', 'a') as file:
            #         file.write(f'{bar.date},{bar.open},{bar.high},{bar.low},'
            #                    f'{bar.close},{bar.barCount},{bar.volume},{bar.average}\n')

            # Collect data as bar for each 5 second frequency over 1 min period
            self.data_collection.append(bar)

            # TODO Need to think about a way to trigger the data on time. currently it's 5 sec delay because of API limitation on time change
            """
            One option I thought is to check the 60 sec on machine time and push the data.
            update: Can't apply this logic, Since the API frequency calls are not consistent
            """
            if self.previous_ts != bar.date:
                if len(self.data_collection) > 1:
                    previous_bar = self.data_collection[-2]
                    with open('realtime_data/data.csv', 'a') as file:
                        file.write(f'{previous_bar.date},{previous_bar.open},{previous_bar.high},{previous_bar.low},'
                                   f'{previous_bar.close},{previous_bar.barCount},{previous_bar.volume},{previous_bar.average}\n')

                self.previous_ts = bar.date
                # Reset the list for next minute of data with 5 sec frequency
                # Reset and adding first bar from new timeframe(e.g. 1min, 5 min) to the collection
                self.data_collection = [bar]


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
