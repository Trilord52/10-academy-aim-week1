import pandas as pd
from textblob import TextBlob

def get_sentiment(headline):
    """Calculate sentiment polarity score using TextBlob."""
    return TextBlob(headline).sentiment.polarity

def compute_returns(stock_df):
    """Compute daily percentage returns from closing prices."""
    stock_df = stock_df.sort_values('Date')
    stock_df['daily_return'] = stock_df['Close'].pct_change() * 100
    return stock_df.dropna()