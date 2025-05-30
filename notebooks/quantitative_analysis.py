import pandas as pd
import numpy as np
import talib
import glob
import os

# Directory containing stock data
data_dir = "data/raw/"
stock_files = glob.glob(os.path.join(data_dir, "*_historical_data.csv"))

# Process each stock file
for file_path in stock_files:
    stock_name = os.path.basename(file_path).replace("_historical_data.csv", "")
    # Skip raw_analyst_ratings.csv
    if stock_name == "raw_analyst_ratings":
        continue
    print(f"\nProcessing stock: {stock_name}")
    
    # Load stock price data
    try:
        stock_df = pd.read_csv(file_path)
        print("Stock price data loaded successfully.")
        print("DataFrame shape:", stock_df.shape)
        print("DataFrame head:\n", stock_df.head())
    except FileNotFoundError:
        print(f"Stock price dataset {file_path} not found.")
        continue

    # Ensure the stock price data has required columns
    required_columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
    if not stock_df.empty and all(col in stock_df.columns for col in required_columns):
        # Convert Date to datetime
        stock_df['Date'] = pd.to_datetime(stock_df['Date'])
        
        # Convert columns to numpy arrays for TA-Lib
        close = stock_df['Close'].to_numpy()
        
        # Calculate Technical Indicators using TA-Lib
        stock_df['SMA_20'] = talib.SMA(close, timeperiod=20)
        stock_df['RSI_14'] = talib.RSI(close, timeperiod=14)
        macd, macd_signal, _ = talib.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)
        stock_df['MACD'] = macd
        stock_df['MACD_Signal'] = macd_signal
        
        print("Technical indicators calculated successfully.")
        print(stock_df.tail())
        
        # Save the processed data
        output_file = f"data/processed/{stock_name}_processed.csv"
        os.makedirs("data/processed", exist_ok=True)
        stock_df.to_csv(output_file, index=False)
        print(f"Saved processed data to {output_file}")
    else:
        print(f"Stock price data in {file_path} must include columns: Date, Open, High, Low, Close, Volume")