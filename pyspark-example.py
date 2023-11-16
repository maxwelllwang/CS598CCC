from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StringType


print("main start")
scala_version = '2.12'
spark_version = '3.4.0'

packages = [
    f'org.apache.spark:spark-sql-kafka-0-10_{scala_version}:{spark_version}',
    'org.apache.kafka:kafka-clients:3.2.1'
]

# Initialize Spark Session
spark = SparkSession.builder \
    .appName("KafkaReadExample") \
    .config("spark.jars.packages", ",".join(packages))\
    .getOrCreate()

# Define Kafka parameters
kafka_topic_name = "my-topic"
kafka_bootstrap_servers = "localhost:9092"  # e.g., "localhost:9092"

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
