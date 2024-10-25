from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import MACD
from surmount.logging import log
from surmount.data import Asset

class TradingStrategy(Strategy):
    def __init__(self):
        # Define the tickers we're interested in
        self.tickers = ["AAPL", "MSFT", "GOOGL", "AMZN"]
        
    @property
    def assets(self):
        # Return the list of assets we're trading
        return self.tickers
    
    @property
    def interval(self):
        # Use daily data for our analysis
        return "1day"
    
    @property
    def data(self):
        # No additional data other than what's provided by base_class is used
        return []
    
    def run(self, data):
        allocation_dict = {}

        # Iterate through each ticker
        for ticker in self.tickers:
            # Calculate MACD and signal lines
            macd_data = MACD(ticker, data["ohlcv"], fast=12, slow=26, signal=9)
            
            if macd_data is None or len(macd_data["MACD"]) < 2 or len(macd_data["signal"]) < 2:
                log(f"Insufficient data for {ticker}")
                continue
            
            # Current and previous MACD values
            macd_line = macd_data["MACD"][-1]
            prev_macd_line = macd_data["MACD"][-2]
            
            # Current and previous signal values
            signal_line = macd_data["signal"][-1]
            prev_signal_line = macd_data["signal"][-2]
            
            # Determine allocation based on MACD crossover
            if macd_line > signal_line and prev_macd_line <= prev_signal_line:
                log(f"Going long on {ticker}")
                allocation_dict[ticker] = 1 / len(self.tickers)  # Allocate equally among tickers
            elif macd_line < signal_line and prev_macd_line >= prev_signal_line:
                log(f"Exiting position (if any) in {ticker}")
                allocation_dict[ticker] = 0  # Exit position
            else:
                # No change in our position for this ticker
                allocation_dict[ticker] = 0

        return TargetAllocation(allocation_dict)