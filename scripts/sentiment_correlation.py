import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
from scipy.stats import pearsonr
import matplotlib.pyplot as plt
from datetime import datetime
from src.utils import get_sentiment, compute_returns

# List of stocks to analyze
stocks = ['AAPL', 'AMZN', 'GOOG', 'MSFT', 'NVDA', 'TSLA', 'META']

try:
    # Load news data
    news_df = pd.read_csv('data/raw/raw_analyst_ratings.csv')
    print("Unique stock symbols in news data:", news_df['stock'].unique())

    # Parse dates with specific format including timezone
    news_df['date'] = pd.to_datetime(news_df['date'], format='%Y-%m-%d %H:%M:%S%z', errors='coerce').dt.date
    news_df = news_df[news_df['date'].notna()]

    # Process each stock
    for stock in stocks:
        try:
            # Load stock data
            stock_df = pd.read_csv(f'data/raw/{stock}_historical_data.csv')

            # Normalize stock dates
            stock_df['Date'] = pd.to_datetime(stock_df['Date'], format='mixed', dayfirst=False).dt.date

            # Filter news for the current stock
            stock_news_df = news_df[news_df['stock'] == stock].copy()

            if stock_news_df.empty:
                print(f"No news data for {stock}, skipping...")
                continue

            # Sentiment analysis
            stock_news_df.loc[:, 'sentiment'] = stock_news_df['headline'].apply(get_sentiment)

            # Aggregate daily sentiment
            daily_sentiment = stock_news_df.groupby('date')['sentiment'].mean().reset_index()

            # Compute daily returns
            stock_df = compute_returns(stock_df)

            # Merge data
            merged_df = pd.merge(daily_sentiment, stock_df, left_on='date', right_on='Date', how='inner')

            if len(merged_df) < 5:
                print(f"Insufficient data points for {stock} (less than 5), skipping...")
                continue

            print(f"{stock} merged_df rows: {len(merged_df)}")
            print(f"{stock} merged_df sample:", merged_df[['date', 'sentiment', 'daily_return']].head())

            # Compute Pearson correlation
            correlation, p_value = pearsonr(merged_df['sentiment'], merged_df['daily_return'])
            print(f"Pearson Correlation ({stock}): {correlation:.3f}, p-value: {p_value:.3f}")

            # Save processed data
            stock_news_df.to_csv(f'data/processed/{stock}_news_aligned.csv', index=False)
            daily_sentiment.to_csv(f'data/processed/{stock}_daily_sentiment.csv', index=False)
            stock_df.to_csv(f'data/processed/{stock}_stock_returns.csv', index=False)

            # Visualization
            plt.figure(figsize=(10, 5))
            plt.plot(merged_df['date'], merged_df['sentiment'], label='Daily Sentiment', color='blue')
            plt.plot(merged_df['date'], merged_df['daily_return'], label='Daily Return (%)', color='orange')
            plt.xlabel('Date')
            plt.ylabel('Value')
            plt.title(f'{stock}: Sentiment vs. Stock Returns')
            plt.legend()
            plt.grid()
            plt.savefig(f'notebooks/figures/{stock}_sentiment_vs_returns.png')
            plt.close()

        except FileNotFoundError as e:
            print(f"Error: Stock data file for {stock} not found - {e}")
        except Exception as e:
            print(f"Error processing {stock}: {e}")

except FileNotFoundError as e:
    print(f"Error: News data file not found - {e}")
except Exception as e:
    print(f"Unexpected error: {e}")