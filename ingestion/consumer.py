from kafka import KafkaConsumer
from cassandra.cluster import Cluster
from textblob import TextBlob
import json

# Connect to Cassandra
cluster = Cluster(['127.0.0.1'])  # Change if your Cassandra IP is different
session = cluster.connect('twitter_keyspace')

# Prepare CQL queries
insert_tweet_cql = """
    INSERT INTO tweets (id_str, created_at, sentiment, text, user_screen_name)
    VALUES (%s, %s, %s, %s, %s)
"""

update_sentiment_count_cql = """
    UPDATE sentiment_counts SET count = count + 1 WHERE sentiment = %s
"""

def analyze_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0:
        return 1  # positive
    elif polarity < 0:
        return -1  # negative
    else:
        return 0  # neutral

def print_sentiment_counts():
    rows = session.execute('SELECT sentiment, count FROM sentiment_counts')
    counts = {1: 0, 0: 0, -1: 0}
    for row in rows:
        counts[row.sentiment] = row.count
    print(f"Sentiment counts => Positive: {counts[1]}, Neutral: {counts[0]}, Negative: {counts[-1]}")

sentiment_labels = {1: "positive", 0: "neutral", -1: "negative"}

# Kafka consumer setup
consumer = KafkaConsumer(
    'tweets_topic',
    bootstrap_servers=['localhost:9092'],  # Default Kafka port
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

counter = 0

print("🟣 Kafka consumer started, listening to tweets...")

for message in consumer:
    tweet = message.value
    try:
        tweet_id = tweet['id_str']
        created_at = tweet['created_at']
        text = tweet['text']
        user_screen_name = tweet['user']['screen_name']

        # Analyze sentiment
        sentiment = analyze_sentiment(text)

        # Insert tweet into Cassandra
        session.execute(insert_tweet_cql, (tweet_id, created_at, sentiment, text, user_screen_name))
        # Update sentiment count
        session.execute(update_sentiment_count_cql, (sentiment,))

        counter += 1
        print(f"Inserted tweet {tweet_id} | Sentiment: {sentiment_labels[sentiment]}")

        if counter % 100 == 0:
            print_sentiment_counts()

    except Exception as e:
        print(f"Error processing tweet {tweet.get('id_str', 'unknown')}: {e}")
