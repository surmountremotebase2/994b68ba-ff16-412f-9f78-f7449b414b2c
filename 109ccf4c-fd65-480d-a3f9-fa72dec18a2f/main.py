from surmount.base_class import Strategy, TargetAllocation
from surmount.data import ConsumerConfidence
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Define our tickers of interest
        self.tickers = ["QQQ", "SPY"]
        # We don't need to add ohlcv data to the data_list, 
        # ConsumerConfidence data is sufficient for our use case
        self.data_list = [ConsumerConfidence()]

    @property
    def assets(self):
        """Specifies the assets the strategy will trade."""
        return self.tickers

    @property
    def interval(self):
        """The frequency at which the strategy will run."""
        # Daily intervals are chosen here as Consumer Confidence data does not update frequently
        return "1day"

    @property
    def data(self):
        """Data required for running the strategy."""
        return self.data_list

    def run(self, data):
        """Defines the core logic of the trading strategy."""
        conf_key = ("consumer_confidence",)
        consumer_confidence = data[conf_key][-1]['value'] if conf_key in data and len(data[conf_key]) > 0 else None
        
        # Default allocation is 50/50 between QQQ and SPY
        allocation_dict = {"QQQ": 0.5, "SPY": 0.5}

        if consumer_confidence is not None:
            log(f"Current Consumer Confidence: {consumer_confidence}")
            # Adjust allocations based on consumer confidence level
            # High consumer confidence (> 100) tilts more towards QQQ
            if consumer_confidence > 100:
                allocation_dict["QQQ"] = 0.6  # Increase allocation to QQQ
                allocation_dict["SPY"] = 0.4
            # Low consumer confidence (< 100) tilts more towards SPY
            else:
                allocation_dict["QQQ"] = 0.4
                allocation_dict["SPY"] = 0.6  # Increase allocation to SPY

        return TargetAllocation(allocation_dict)