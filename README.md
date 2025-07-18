# Sentiment Analysis Data Pipeline Example

## Overview
This project demonstrates a sentiment analysis data engineering pipeline using the Sentiment-10000 dataset.
It includes:
- Data ingestion using Kafka in Docker
- MongoDB for unstructured data storage with CRUD operations
- Spark batch processing for aggregation
- Cloud integration placeholders (AWS)
- Documentation

## Folder Structure
- ingestion/: Kafka producer and Dockerfile
- storage/: MongoDB CRUD script
- processing/: Spark batch job
- cloud/: Cloud configuration placeholders

## Setup Instructions
1. Start Kafka and Zookeeper (can be done using Docker Compose or standalone Docker containers)
2. Build and run the ingestion Docker container to simulate data ingestion
3. Start MongoDB and run the CRUD script to test data storage
4. Run the Spark aggregation script with PySpark installed

## Future Work
- Implement real-time streaming ingestion and processing
- Integrate with cloud services (AWS MSK, DocumentDB, EMR)
- Add visualization dashboards