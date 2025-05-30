10 Academy AIM Week 1: Financial News and Stock Price Correlation Analysis
Project Overview
This project, developed as part of the 10 Academy AIM Week 1 challenge, aims to analyze the correlation between financial news sentiment and stock price movements for Nova Financial Solutions. The analysis focuses on seven major tech stocks: AAPL, AMZN, GOOG, MSFT, NVDA, TSLA, and META. The project is structured into three tasks:

Task 1: Environment setup and exploratory data analysis (EDA) of financial news data.
Task 2: Quantitative analysis using technical indicators (e.g., SMA, RSI, MACD) with libraries like TA-Lib.
Task 3: Sentiment analysis of news headlines using TextBlob and correlation analysis with stock price movements.

Repository Structure

data/raw/: Raw data files (e.g., raw_analyst_ratings.csv, stock data CSVs).
data/processed/: Processed data (e.g., sentiment scores, stock returns).
scripts/: Python scripts for data processing and analysis.
download_stocks.py: Downloads historical stock data.
sentiment_correlation.py: Performs sentiment and correlation analysis.


notebooks/: Jupyter notebooks for EDA and visualizations.
notebooks/figures/: Generated plots (e.g., GOOG_sentiment_vs_returns.png).
src/: Source code for modular functions (if applicable).

Prerequisites

Python 3.7+
Dependencies: pandas, numpy, matplotlib, textblob, scipy, yfinance, ta-lib (optional for Task 2)

Installation

Clone the repository:git clone https://github.com/Trilord52/10-academy-aim-week1.git


Navigate to the project directory:cd 10-academy-aim-week1


Create a virtual environment (optional but recommended):python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


Install dependencies:pip install pandas numpy matplotlib textblob scipy yfinance

Note: If using TA-Lib for Task 2, follow installation instructions here.

Usage

Download Stock Data:

Run the script to download historical stock data:python scripts/download_stocks.py

This saves data to data/raw/ (e.g., AAPL_historical_data.csv).

Run Sentiment and Correlation Analysis:

Execute the main analysis script:python scripts/sentiment_correlation.py

Outputs:
Processed files in data/processed/ (e.g., GOOG_daily_sentiment.csv).
Plots in notebooks/figures/ (e.g., GOOG_sentiment_vs_returns.png).
Terminal output of Pearson correlations (e.g., Pearson Correlation (GOOG): -0.089, p-value: 0.886).


Key Findings

Task 1 (EDA): News publication peaks on Mondays/Thursdays, 9 AM–12 PM EST. Frequent terms: “earnings,” “price target.”
Task 2 (Quantitative Analysis): Technical indicators (e.g., RSI, MACD) computed for all stocks. Example: TSLA showed overbought conditions (RSI > 70).
Task 3 (Sentiment Correlation):
GOOG: Weak negative correlation (-0.089, p-value: 0.886), not significant.
NVDA: Weak positive correlation (0.176, p-value: 0.824), but skipped due to insufficient data points (< 5).
AAPL, AMZN, TSLA: Skipped due to sparse data.
MSFT, META: No news data in dataset.



Limitations

Sparse overlap between news and stock data dates (e.g., AAPL/AMZN with only 2 points).
Missing news data for MSFT and META (possible ticker mismatch, e.g., ‘MS’, ‘FB’).
Sentiment analysis with TextBlob may not capture financial nuances.

Contact
Tinbite Yonas 