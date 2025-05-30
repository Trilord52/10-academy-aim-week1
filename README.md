10 Academy - AIM - Week 1 Project
Introduction
This repository contains the codebase and resources for the "10 Academy - AIM - Week 1" project, aimed at predicting stock price movements using financial news sentiment. The project leverages data pipelines, exploratory data analysis (EDA), and quantitative analysis to build a foundation for sentiment-based stock prediction.
Project Structure

data/raw/: Raw stock and news data (local only, excluded via .gitignore).

data/processed/: Processed stock data with technical indicators (local only).

notebooks/: Jupyter notebooks and generated figures (e.g., figures/ with visualizations).

quantitative_analysis.py: Python script for quantitative analysis using TA-Lib and manual financial metrics.

Progress

Task 1: Exploratory Data Analysis (EDA)

Analyzed news dataset to extract headline length statistics, top publishers, domains, and keywords.

Generated visualizations: daily_publication_frequency.png and hourly_publication_frequency.png.

Task 2: Quantitative Analysis

Implemented quantitative analysis using TA-Lib for technical indicators (SMA_20, RSI_14, MACD).

Calculated annualized return and volatility manually due to pynance limitations.

Created visualizations (Close Price with SMA, RSI, MACD) saved in notebooks/figures/.

Challenges: Resolved pynance module issue and large file size problem by excluding .csv files via .gitignore.

Next Steps

Task 3: Sentiment Analysis: Develop a sentiment analysis model to correlate news sentiment with stock price movements.

Key Focus: Integrate sentiment scores with quantitative metrics to enhance prediction accuracy.

Priority: Clean and preprocess news data for sentiment extraction.

Setup and Usage

Clone the repository: git clone https://github.com/Trilord52/10-academy-aim-week1.git
Install dependencies: pip install -r requirements.txt
Run the quantitative analysis: python quantitative_analysis.py
Contributors: Trilord52