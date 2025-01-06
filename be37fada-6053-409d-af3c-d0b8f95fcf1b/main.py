from surmount.base_class import Strategy, TargetAllocation
from surmount.data import SocialSentiment, Asset
import pandas as pd

class TradingStrategy(Strategy):
    def __init__(self):
        # Define the asset ticker
        self.ticker = "AAPL"
        # Define the list of data requirements, including social sentiment
        self.data_list = [SocialSentiment(self.ticker)]
        
    @property
    def interval(self):
        # Define the data interval
        return "1day"
        
    @property
    def assets(self):
        # List of assets this strategy will trade
        return [self.ticker]
    
    @property
    def data(self):
        # Data requirements for the strategy
        return self.data_list
    
    def run(self, data):
        # Initialize allocation dictionary with a neutral stance
        allocation_dict = {self.ticker: 0.5}
        
        # Access the latest social sentiment and trading volume data
        sentiment_data = data[("social_sentiment", self.ticker)]
        if sentiment_data and len(sentiment_data) > 0:
            latest_sentiment = sentiment_data[-1]["twitterSentiment"]
            
            # Basic strategy logic based on sentiment
            if latest_sentiment > 0.6:
                # Positive sentiment (> 0.6) suggests buying pressure; increase allocation
                allocation_dict[self.ticker] = 0.7
            elif latest_sentiment < 0.4:
                # Negative sentiment (< 0.4) suggests selling pressure; decrease allocation
                allocation_dict[self.ticker] = 0.3
        
        # Return the target allocation based on the strategy's logic
        return TargetAllocation(allocation_dict)