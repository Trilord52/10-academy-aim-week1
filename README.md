10 Academy - AIM - Week 1 Project
Introduction
This repository contains the codebase and resources for the "10 Academy - AIM - Week 1" project, aimed at predicting stock price movements using financial news sentiment. The project leverages data pipelines, exploratory data analysis (EDA), and quantitative analysis to build a foundation for sentiment-based stock prediction. By understanding how news sentiment influences stock prices, this analysis can help traders and financial institutions make informed decisions, identify market trends, and manage risks effectively in real-world trading scenarios.
Project Structure

data/raw/: Raw stock and news data (local only, excluded via .gitignore).
data/processed/: Processed stock data with technical indicators (local only).
notebooks/: Jupyter notebooks and generated figures (e.g., figures/ with visualizations like daily_publication_frequency.png).
quantitative_analysis.py: Python script for quantitative analysis using TA-Lib and manual financial metrics.

Progress
Task 1: Exploratory Data Analysis (EDA)

Objective: Analyzed a news dataset (1,407,328 rows) to understand publication patterns and content focus.
Methods: Used pandas to compute headline length statistics, identify top publishers, extract domains, and detect keywords.
Findings:
Top publishers included Benzinga and The Street, indicating a focus on financial news relevant to stock markets.
Daily publication frequency showed peaks during market opening hours (9 AM–12 PM EST), suggesting news aligns with trading activity.
Visualizations generated: daily_publication_frequency.png and hourly_publication_frequency.png.


Challenges: Handled large dataset size by optimizing data loading and filtering processes.

Task 2: Quantitative Analysis

Objective: Performed quantitative analysis on stock data to compute technical indicators and financial metrics.
Methods:
Used TA-Lib to calculate SMA_20, RSI_14, and MACD for stocks like AAPL, AMZN, and GOOG.
Calculated annualized return and volatility manually using pandas and numpy due to pynance lacking a stats module.
Generated visualizations (Close Price with SMA, RSI, MACD) saved in notebooks/figures/.


Findings:
RSI_14 indicated overbought conditions for TSLA (RSI > 70) on several days, suggesting potential price corrections.
MACD crossovers for GOOG aligned with short-term price trends, validating its use for trend analysis.


Challenges:
Resolved pynance limitation by implementing custom financial metric calculations.
Addressed large file size issue (raw_analyst_ratings.csv, 311.40 MB) by excluding .csv files via .gitignore and rewriting Git history.



Next Steps

Task 3: Sentiment Analysis:
Develop a sentiment analysis model to quantify news sentiment and correlate it with stock price movements.
Rationale: Sentiment scores can capture market mood, improving prediction accuracy by identifying bullish or bearish trends driven by news.


Key Focus: Integrate sentiment scores with quantitative metrics (e.g., RSI, MACD) to create a hybrid prediction model.
Significance: Combining sentiment and technical indicators can provide a more robust signal for stock price movements, reducing false positives.


Priority: Clean and preprocess news data for sentiment extraction, ensuring high-quality input for the model.
Reason: Accurate sentiment analysis depends on clean data, free from noise like duplicate headlines or irrelevant articles.



Setup and Usage

Clone the Repository:git clone https://github.com/Trilord52/10-academy-aim-week1.git


Install Dependencies:
Ensure you have Python 3.8+ installed.
Install required packages:pip install pandas numpy matplotlib talib




Run the Quantitative Analysis:python quantitative_analysis.py


This script processes stock data, computes indicators, and generates visualizations.



Contributors

Trilord52(Tinbite Yonas)