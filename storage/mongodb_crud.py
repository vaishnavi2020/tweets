# storage/mongodb_crud.py
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['sentiment_db']
collection = db['tweets']

def insert_tweet(tweet_doc):
    collection.insert_one(tweet_doc)
    print('Inserted:', tweet_doc)

def find_tweets_by_sentiment(sentiment):
    results = collection.find({'sentiment': sentiment})
    for r in results:
        print(r)

def update_tweet_sentiment(tweet_id, new_sentiment):
    collection.update_one({'tweet_id': tweet_id}, {'$set': {'sentiment': new_sentiment}})
    print(f'Updated tweet {tweet_id} sentiment to {new_sentiment}')

def delete_tweet(tweet_id):
    collection.delete_one({'tweet_id': tweet_id})
    print(f'Deleted tweet {tweet_id}')

if __name__ == '__main__':
    tweet = {'tweet_id': '12345', 'sentiment': '1', 'tweet': 'This is a great product!'}
    insert_tweet(tweet)
    find_tweets_by_sentiment('1')
    update_tweet_sentiment('12345', '0')
    delete_tweet('12345')