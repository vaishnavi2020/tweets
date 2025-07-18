# processing/spark_aggregation.py
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, count

def main():
    spark = SparkSession.builder.appName("SentimentAggregation").getOrCreate()
    df = spark.read.csv('sentiment_10000.csv', header=True, inferSchema=True)
    df = df.withColumn('sentiment', col('sentiment').cast('int'))
    
    # Aggregate: average sentiment score per sentiment type
    agg_df = df.groupBy('sentiment').agg(count('*').alias('count'))
    agg_df.show()
    
    spark.stop()

if __name__ == '__main__':
    main()