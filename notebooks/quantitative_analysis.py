import pandas as pd
import numpy as np
import talib
import glob
import os
import matplotlib.pyplot as plt
import logging
from datetime import datetime

# Setup logging to track progress and errors
start_time = datetime.now()
logging.basicConfig(
    filename='quantitative_analysis.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logging.info("Starting quantitative analysis script.")
print(f"Starting analysis at {start_time.strftime('%Y-%m-%d %H:%M:%S')}")

# Configuration
DATA_DIR = "data/raw/"  # Input directory
OUTPUT_DIR = "data/processed/"  # Output directory for processed data
PLOT_DIR = "notebooks/figures/"  # Output directory for plots
TRADING_DAYS_PER_YEAR = 252  # Trading days per year

# List for summary stats
summary_stats = []

# Section: Data Loading
# Find all stock data files ending with _historical_data.csv
stock_files = glob.glob(os.path.join(DATA_DIR, "*_historical_data.csv"))
logging.info(f"Found {len(stock_files)} stock files to process.")
print(f"Found {len(stock_files)} stock files to process.")

for file_path in stock_files:
    stock_name = os.path.basename(file_path).replace("_historical_data.csv", "")
    
    # Skip non-stock files
    if stock_name == "raw_analyst_ratings":
        logging.info("Skipping raw_analyst_ratings.csv.")
        continue
    
    print(f"\nProcessing stock: {stock_name}")
    logging.info(f"Processing stock: {stock_name}")

    # Section: Load and Validate Data
    # Load stock data and validate required columns
    try:
        stock_df = pd.read_csv(file_path)
        print("Stock price data loaded successfully.")
        print("DataFrame shape:", stock_df.shape)
        print("DataFrame head:\n", stock_df.head())
        logging.info(f"Loaded {stock_name} data with shape {stock_df.shape}")
    except Exception as e:
        print(f"Failed to load {file_path}: {e}")
        logging.error(f"Failed to load {file_path}: {e}")
        continue

    required_columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
    if stock_df.empty:
        print(f"Stock price data for {stock_name} is empty. Skipping.")
        logging.warning(f"Stock price data for {stock_name} is empty.")
        continue
    if not all(col in stock_df.columns for col in required_columns):
        print(f"Stock price data in {file_path} must include columns: {required_columns}")
        logging.warning(f"Missing required columns in {stock_name}: {required_columns}")
        continue

    # Section: Data Preparation
    # Convert Date to datetime
    stock_df['Date'] = pd.to_datetime(stock_df['Date'])
    logging.info(f"Converted Date column to datetime for {stock_name}.")

    # Section: Technical Indicators with TA-Lib
    # Calculate SMA_20, RSI_14, and MACD using TA-Lib
    close = stock_df['Close'].to_numpy()
    if (close <= 0).any():
        print(f"Warning: Invalid Close prices for {stock_name}. Skipping indicator calculations.")
        logging.warning(f"Invalid Close prices for {stock_name}.")
        continue
    stock_df['SMA_20'] = talib.SMA(close, timeperiod=20)
    stock_df['RSI_14'] = talib.RSI(close, timeperiod=14)
    macd, macd_signal, _ = talib.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)
    stock_df['MACD'] = macd
    stock_df['MACD_Signal'] = macd_signal

    print("Technical indicators calculated successfully.")
    print(stock_df.tail())
    logging.info(f"Calculated technical indicators for {stock_name}.")

    # Section: Financial Metrics
    # Calculate annualized return and volatility manually (pynance lacks stats module)
    if 'Adj Close' not in stock_df.columns:
        print(f"Warning: 'Adj Close' column missing for {stock_name}. Using 'Close' instead.")
        logging.warning(f"'Adj Close' column missing for {stock_name}. Using 'Close'.")
        adj_close = stock_df['Close']
    else:
        adj_close = stock_df['Adj Close']

    if (adj_close <= 0).any():
        print(f"Warning: Invalid Adj Close prices for {stock_name}. Skipping financial metrics.")
        logging.warning(f"Invalid Adj Close prices for {stock_name}.")
        continue

    adj_returns = adj_close.pct_change().dropna()
    if len(adj_returns) > 0:
        annualized_return = ((1 + adj_returns.mean()) ** TRADING_DAYS_PER_YEAR) - 1
        volatility = adj_returns.std() * np.sqrt(TRADING_DAYS_PER_YEAR)
        print(f"Annualized Return for {stock_name} (using Adj Close): {annualized_return:.4f}")
        print(f"Volatility for {stock_name} (using Adj Close): {volatility:.4f}")
        logging.info(f"Annualized Return for {stock_name}: {annualized_return:.4f}, Volatility: {volatility:.4f}")
        
        summary_stats.append({
            'Stock': stock_name,
            'Annualized Return': annualized_return,
            'Volatility': volatility
        })
    else:
        print(f"No returns data available for {stock_name} to calculate financial metrics.")
        logging.warning(f"No returns data for {stock_name} to calculate financial metrics.")

    # Section: Visualization
    # Plot Close Price with SMA, RSI, and MACD
    plt.figure(figsize=(12, 8))
    
    plt.subplot(3, 1, 1)
    plt.plot(stock_df['Date'], stock_df['Close'], label='Close Price', color='blue')
    plt.plot(stock_df['Date'], stock_df['SMA_20'], label='SMA_20', color='orange')
    plt.title(f'{stock_name} Close Price and SMA_20')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True)

    plt.subplot(3, 1, 2)
    plt.plot(stock_df['Date'], stock_df['RSI_14'], label='RSI_14', color='purple')
    plt.axhline(70, linestyle='--', color='red', alpha=0.5, label='Overbought (70)')
    plt.axhline(30, linestyle='--', color='green', alpha=0.5, label='Oversold (30)')
    plt.title(f'{stock_name} RSI_14')
    plt.xlabel('Date')
    plt.ylabel('RSI')
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True)

    plt.subplot(3, 1, 3)
    plt.plot(stock_df['Date'], stock_df['MACD'], label='MACD', color='blue')
    plt.plot(stock_df['Date'], stock_df['MACD_Signal'], label='MACD Signal', color='orange')
    plt.axhline(0, linestyle='--', color='black', alpha=0.5, label='Zero Line')
    plt.title(f'{stock_name} MACD')
    plt.xlabel('Date')
    plt.ylabel('MACD')
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    os.makedirs(PLOT_DIR, exist_ok=True)
    output_plot = os.path.join(PLOT_DIR, f"{stock_name}_indicators.png")
    plt.savefig(output_plot)
    plt.close()
    print(f"Saved plot to {output_plot}")
    logging.info(f"Saved plot for {stock_name} to {output_plot}")

    # Section: Save Processed Data
    # Save processed DataFrame with indicators
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_file = os.path.join(OUTPUT_DIR, f"{stock_name}_processed.csv")
    stock_df.to_csv(output_file, index=False)
    print(f"Saved processed data to {output_file}")
    logging.info(f"Saved processed data for {stock_name} to {output_file}")

# Section: Summary Statistics
# Print summary table of financial metrics, sorted by annualized return
if summary_stats:
    print("\nSummary of Financial Metrics for All Stocks (Sorted by Annualized Return):")
    summary_df = pd.DataFrame(summary_stats)
    summary_df = summary_df.sort_values(by='Annualized Return', ascending=False)
    print(summary_df.to_string(index=False))
    logging.info("Printed summary of financial metrics.")
else:
    print("\nNo financial metrics to summarize.")
    logging.warning("No financial metrics to summarize.")

# Log completion and runtime
end_time = datetime.now()
logging.info("Quantitative analysis script completed successfully.")
print(f"\nAnalysis complete for all stocks! Finished at {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Total runtime: {end_time - start_time}")