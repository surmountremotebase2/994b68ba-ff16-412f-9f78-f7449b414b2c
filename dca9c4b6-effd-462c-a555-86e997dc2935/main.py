from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA
from surmount.data import Asset, InstitutionalOwnership, SocialSentiment

class TradingStrategy(Strategy):
    def __init__(self):
        self.tickers = ["AAPL"]
        # Adding the necessary data objects to the data list
        self.data_list = [
            InstitutionalOwnership("AAPL"), 
            SocialSentiment("AAPL")
        ]

    @property
    def interval(self):
        return "1day"

    @property
    def assets(self):
        return self.tickers

    @property
    def data(self):
        return self.data_list

    def run(self, data):
        # Default allocation is 0, meaning do not hold the asset
        allocation_dict = {"AAPL": 0}
        
        # Check if we have the necessary data points to make a decision
        inst_ownership_data = data.get(("institutional_ownership", "AAPL"), [])
        sentiment_data = data.get(("social_sentiment", "AAPL"), [])
        
        # Fetch the ohlcv data for AAPL to compute the SMA
        ohlcv_data = data.get("ohlcv", {}).get("AAPL", [])
        sma_50 = SMA("AAPL", ohlcv_data, length=50)
        
        if not sma_50 or not ohlcv_data:
            return TargetAllocation(allocation_dict) # Return with 0 allocation if data is missing
        
        latest_close_price = ohlcv_data[-1]["close"]
        
        # Check the conditions for a buy signal
        if inst_ownership_data and sentiment_data:
            # Checking the latest available data for trends
            recent_ownership_change = inst_ownership_data[-1].get("ownershipPercentChange", 0)
            recent_sentiment = sentiment_data[-1].get("twitterSentiment", 0.5)  # Default to neutral sentiment if not available
            
            # Buy signal conditions
            if recent_ownership_change > 0 and recent_sentiment > 0.5 and latest_close_price > sma_50[-1]:
                allocation_dict["AAPL"] = 0.1  # Allocate 10% of the portfolio to AAPL
                
        return TargetAllocation(allocation_dict)