from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # List of tickers our strategy will evaluate
        self.tickers = ["QQQ"]
        
    @property
    def assets(self):
        # Define which assets we are interested in
        return self.tickers

    @property
    def interval(self):
        # Data frequency, daily for long-term moving averages
        return "1day"

    def run(self, data):
        # Dictionary to hold our target allocations
        allocation_dict = {}
        
        for ticker in self.tickers:
            # Calculating the 50-day and 200-day SMA
            sma_50 = SMA(ticker, data["ohlcv"], 50)
            sma_200 = SMA(ticker, data["ohlcv"], 200)
            
            # Ensure we have enough data points for both SMAs
            if sma_50 and sma_200 and len(sma_50) > 199 and len(sma_200) > 199:
                # Check if the 50-day SMA is above the 200-day SMA
                if sma_50[-1] > sma_200[-1]:
                    # If so, allocate 100% of our portfolio to this asset
                    allocation_dict[ticker] = 1.0
                else:
                    # Otherwise, do not hold this asset
                    allocation_dict[ticker] = 0.0
            else:
                # If not enough data, do not allocate to this asset
                allocation_dict[ticker] = 0.0
        
        # Return the target allocation
        return TargetAllocation(allocation_dict)