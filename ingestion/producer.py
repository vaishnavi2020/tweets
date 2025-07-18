import csv
from kafka import KafkaProducer
import json
import time

def read_tweets(filepath):
    with open(filepath, 'r', encoding='latin-1') as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            print(f"DEBUG: Row {i}: {row}")
            
            if len(row) < 6:
                print(f"Skipped row {i}: insufficient columns")
                continue

            sentiment = row[0]
            tweet_id = row[1]
            created_at = row[2]
            query = row[3].strip()
            username = row[4].strip()
            tweet_text = row[5]

            # Commented out NO_QUERY skip to send all tweets
            # if query.upper() == "NO_QUERY":
            #     print(f"Skipped NO_QUERY row at index {i}")
            #     continue

            yield {
                'id_str': tweet_id,
                'user': {'screen_name': username},
                'text': tweet_text,
                'created_at': created_at,
                'sentiment': sentiment
            }

def main():
    producer = KafkaProducer(
        bootstrap_servers='localhost:9092',
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

    filepath = '/Users/tejasrielabotharam/Downloads/sentiment_analysis_pipeline/ingestion/sentiment_10000.csv'

    count = 0
    for tweet in read_tweets(filepath):
        producer.send('tweets_topic', tweet)
        print(f"Sent tweet #{count+1}: {tweet}")
        count += 1
        time.sleep(0.5)  # small delay to avoid flooding Kafka

    producer.flush()
    print(f"Finished sending {count} tweets")

if __name__ == "__main__":
    main()
