import eventlet
eventlet.monkey_patch()

from flask import Flask, render_template
from flask_socketio import SocketIO
from kafka import KafkaConsumer
from cassandra.cluster import Cluster
import json
import time 

app = Flask(__name__)
socketio = SocketIO(app, async_mode='eventlet')

# Connect to Cassandra
cluster = Cluster(['127.0.0.1'])  # use correct IP if needed
session = cluster.connect('twitter_keyspace')

# 🔵 ADD THIS RIGHT AFTER Cassandra CONNECTION
sentiment_map = {
    1: "Positive",
    0: "Neutral",
    -1: "Negative"
}

def kafka_listener():
    consumer = KafkaConsumer(
        'tweets_topic',
        bootstrap_servers='localhost:9092',
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        value_deserializer=lambda b: json.loads(b.decode('utf-8'))
    )
    print("🟣 Kafka listener started, awaiting messages…")

    for msg in consumer:
        tweet = msg.value
        tweet_id = tweet['id_str']

        try:
            # 🔵 Get sentiment from Cassandra
            row = session.execute(
                "SELECT sentiment FROM tweets WHERE id_str=%s LIMIT 1",
                [tweet_id]
            ).one()

            if row:
                tweet['sentiment'] = row.sentiment
                # 🔵 ADD THIS INSIDE THE LOOP AFTER YOU HAVE row.sentiment
                tweet['sentiment_label'] = sentiment_map.get(row.sentiment, "Unknown")
            else:
                tweet['sentiment'] = 0
                tweet['sentiment_label'] = "Unknown"

            print(f"🟢 Got tweet {tweet_id} | Sentiment: {tweet['sentiment_label']}")
            socketio.emit('new_tweet', tweet)

            time.sleep(2)

            

        except Exception as e:
            print(f"🔴 Error fetching sentiment for tweet {tweet_id}: {e}")

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    socketio.start_background_task(kafka_listener)
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
