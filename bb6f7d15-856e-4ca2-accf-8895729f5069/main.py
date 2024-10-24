from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI, SMA
from surmount.data import Asset, SocialSentiment

class TradingStrategy(Strategy):
    def __init__(self):
        self.tickers = ["AAPL"]  # Focusing on Apple for this strategy
        # SocialSentiment data will be used in addition to technical indicators
        self.data_list = [SocialSentiment(i) for i in self.tickers]

    @property
    def interval(self):
        return "1day"  # Using daily data for analysis

    @property
    def assets(self):
        return self.tickers

    @property
    def data(self):
        return self.data_list

    def run(self, data):
        sentiment = data[("social_sentiment", "AAPL")]  # Accessing social sentiment data
        # Assuming a simple average sentiment score exists; one could also implement a more detailed sentiment analysis
        average_sentiment = sum(d['stocktwitsSentiment'] for d in sentiment) / len(sentiment)
        
        # Initialize allocation with no position
        allocation_dict = {"AAPL": 0}

        # Check data availability for technical analysis
        if "ohlcv" in data and len(data["ohlcv"]) > 20:  # Ensure enough data for SMA calculation
            sma20 = SMA("AAPL", data["ohlcv"], 20)[-1]  # 20-day simple moving average
            current_price = data["ohlcv"][-1]["AAPL"]["close"]  # Current closing price

            # Strategy logic: Go if the current price is above the 20-day SMA and average sentiment is positive (>0.5)
            if current_price > sma20 and average_sentiment > 0.5:
                allocation_dict["AAPL"] = 1  # Full allocation

        # Returning the target allocation for the asset(s)
        return TargetAllocation(allocation_dict)