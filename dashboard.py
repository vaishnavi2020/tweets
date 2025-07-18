import streamlit as st
from cassandra.cluster import Cluster
import pandas as pd
import time

cluster = Cluster(['127.0.0.1'])
session = cluster.connect('twitter_keyspace')

def get_sentiment_counts():
    rows = session.execute('SELECT sentiment, count FROM sentiment_counts')
    counts = {1: 0, 0: 0, -1: 0}
    for row in rows:
        counts[row.sentiment] = row.count
    return counts

def get_latest_tweets(limit=10):
    # Adjust the query as per your table schema and available columns
    rows = session.execute(f"SELECT id_str, created_at, sentiment, text, user_screen_name FROM tweets LIMIT {limit}")
    tweets = []
    for row in rows:
        tweets.append({
            "Time": row.created_at,
            "User": row.user_screen_name,
            "Text": row.text,
            "Sentiment": sentiment_labels.get(row.sentiment, "Unknown")
        })
    return tweets

st.title("Live Sentiment Dashboard")

# Set up auto-refresh interval (in seconds)
refresh_interval = 5

# Use session state to store last refresh time
if 'last_refresh' not in st.session_state:
    st.session_state['last_refresh'] = time.time()

# Auto-refresh logic
if time.time() - st.session_state['last_refresh'] > refresh_interval:
    st.session_state['last_refresh'] = time.time()
    st.experimental_rerun = getattr(st, 'experimental_rerun', lambda: None)
    try:
        st.experimental_rerun()
    except Exception:
        pass


# Track sentiment counts history in session state for live graph
if 'sentiment_history' not in st.session_state:
    st.session_state['sentiment_history'] = []

counts = get_sentiment_counts()
st.write(f"Positive: {counts[1]}, Neutral: {counts[0]}, Negative: {counts[-1]}")

# Append current counts to history
from datetime import datetime
st.session_state['sentiment_history'].append({
    'time': datetime.now().strftime('%H:%M:%S'),
    'Positive': counts[1],
    'Neutral': counts[0],
    'Negative': counts[-1]
})

# Keep only the last 30 points for clarity
if len(st.session_state['sentiment_history']) > 30:
    st.session_state['sentiment_history'] = st.session_state['sentiment_history'][-30:]

# Show live sentiment trend as a line chart
history_df = pd.DataFrame(st.session_state['sentiment_history'])
history_df = history_df.set_index('time')
st.line_chart(history_df)

# Show live sentiment analysis as a bar chart
sentiment_labels = {1: "Positive", 0: "Neutral", -1: "Negative"}
chart_data = pd.DataFrame({
    "Sentiment": [sentiment_labels[k] for k in counts.keys()],
    "Count": [counts[k] for k in counts.keys()]
})
chart_data = chart_data.set_index("Sentiment")
st.bar_chart(chart_data)

# Manual refresh button (optional)
st.button("Refresh")

# Show latest tweets and their sentiment
st.subheader("Latest Tweets and Sentiment Analysis")
tweets = get_latest_tweets(10)
if tweets:
    st.dataframe(pd.DataFrame(tweets))
else:
    st.write("No tweets available.")