import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk

# Download NLTK data
nltk.download('punkt')
nltk.download('stopwords')

# Load the CSV data
df = pd.read_csv("data/raw/raw_analyst_ratings.csv")
print("DataFrame shape:", df.shape)
print("DataFrame head:\n", df.head())

# --- Data Cleaning ---
# Normalize date formats
df['date'] = pd.to_datetime(df['date'], errors='coerce', utc=True)
df = df.dropna(subset=['date'])
print("After date parsing, DataFrame shape:", df.shape)
print("First few dates:\n", df['date'].head())
print("Date column type:", df['date'].dtype)

# Extract date and hour for time series analysis
df['date_only'] = df['date'].dt.date
df['hour'] = df['date'].dt.hour

# Clean publisher: Extract domain if it's an email
def extract_domain(publisher):
    if isinstance(publisher, str) and '@' in publisher:
        return publisher.split('@')[1]
    return publisher

df['publisher_domain'] = df['publisher'].apply(extract_domain)

# --- Descriptive Statistics ---
# 1. Headline length statistics
df['headline_length'] = df['headline'].apply(lambda x: len(str(x).split()))
headline_stats = {
    'Mean': df['headline_length'].mean(),
    'Median': df['headline_length'].median(),
    'Min': df['headline_length'].min(),
    'Max': df['headline_length'].max()
}
print("Headline Length Statistics:", headline_stats)

# 2. Articles per publisher
publisher_counts = df['publisher'].value_counts()
print("\nTop 10 Publishers by Article Count:")
print(publisher_counts.head(10))

# 3. Articles per publisher domain
domain_counts = df['publisher_domain'].value_counts()
print("\nTop 10 Publisher Domains by Article Count:")
print(domain_counts.head(10))

# --- Time Series Analysis ---
# 1. Publication frequency over time (daily)
daily_counts = df.groupby('date_only').size()
plt.figure(figsize=(10, 6))
daily_counts.plot()
plt.title('Daily Article Publication Frequency')
plt.xlabel('Date')
plt.ylabel('Number of Articles')
plt.grid(True)
plt.savefig('notebooks/figures/daily_publication_frequency.png')
plt.close()

# 2. Publication by hour
hourly_counts = df.groupby('hour').size()
plt.figure(figsize=(10, 6))
hourly_counts.plot(kind='bar')
plt.title('Article Publication by Hour')
plt.xlabel('Hour of Day')
plt.ylabel('Number of Articles')
plt.grid(True)
plt.savefig('notebooks/figures/hourly_publication_frequency.png')
plt.close()

# --- Text Analysis (Keyword Extraction) ---
stop_words = set(stopwords.words('english'))
def extract_keywords(headline):
    if not isinstance(headline, str):
        return []
    tokens = word_tokenize(headline.lower())
    keywords = [word for word in tokens if word.isalnum() and word not in stop_words]
    return keywords

# Extract keywords from a sample for interim report
sample_df = df.head(10000)
all_keywords = []
sample_df['headline'].apply(lambda x: all_keywords.extend(extract_keywords(x)))
keyword_counts = Counter(all_keywords)
top_keywords = keyword_counts.most_common(10)
print("\nTop 10 Keywords in Headlines (from sample):")
print(top_keywords)

# Summary of findings for the report
summary = {
    "headline_stats": headline_stats,
    "top_publishers": publisher_counts.head(5).to_dict(),
    "top_domains": domain_counts.head(5).to_dict(),
    "top_keywords": top_keywords
}
print("\nSummary for Interim Report:")
print(summary)