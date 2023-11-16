from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StringType

# Initialize Spark Session
spark = SparkSession.builder \
    .appName("KafkaReadExample") \
    .getOrCreate()

# Define Kafka parameters
kafka_topic_name = "your_kafka_topic"
kafka_bootstrap_servers = "your_kafka_bootstrap_server"  # e.g., "localhost:9092"

# Read from Kafka
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
    .option("subscribe", kafka_topic_name) \
    .load()

# Select the value field and cast it to string
df = df.selectExpr("CAST(value AS STRING)")

# Print to console
query = df.writeStream \
    .outputMode("append") \
    .format("console") \
    .start()

query.awaitTermination()
