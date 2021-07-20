from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.wrapper import BarData
from ibapi.contract import Contract
from ibapi.client import TickAttribLast, TickerId, TickAttribBidAsk
import sys
import datetime
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
        print(bar)

    def historicalDataUpdate(self, reqId: int, bar: BarData):
        # With the 5sec refresh, this will be one of the filter to avoid over loaded responses in analysis
        if bar.volume > 0:
            # Collect data over 5 second frequency over 1 min period
            self.data_collection.append(bar)

            if self.previous_ts != bar.date:
                if len(self.data_collection) > 1:
                    previous_bar = self.data_collection[-2]
                    print(previous_bar)

                self.previous_ts = bar.date
                # Reset the list for next minute of data with 5 sec frequency
                # Reset and adding first bar from new minute to the collection
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

    # Request historical candles
    app.reqHistoricalData(1009, contract, "", "1 D", "1 min", "TRADES", 0, 1, True, [])
    app.run()


main()
