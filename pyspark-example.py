from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, udf
from pyspark.sql.types import StringType, IntegerType, BooleanType,FloatType, StructType, StructField, DoubleType
import time 
import random


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

nyc_taxi_topic_name = "nyc-taxi"


# Read from Kafka
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
    .option("subscribe", nyc_taxi_topic_name) \
    .load()

schema = StructType([
    StructField("time_ns", DoubleType(), True),
    StructField("tpep_pickup_datetime", FloatType(), True),
    StructField("tpep_dropoff_datetime", FloatType(), True),
    StructField("passenger_count", IntegerType(), True),
    StructField("trip_distance", FloatType(), True),
    StructField("fare_amount", FloatType(), True),
    StructField("total_amount", FloatType(), True),
    StructField("sparkpi", IntegerType(), True),
])

json_df = df.select(from_json(col("value").cast("string"), schema).alias("data")).select("data.*")


def estimate_pi(num_samples):
    inside_circle = 0

    for _ in range(num_samples):
        x, y = random.uniform(0, 1), random.uniform(0, 1)
        distance = x**2 + y**2
        if distance <= 1:
            inside_circle += 1
    return 4 * inside_circle / num_samples

def calculate_average_speed_mph(start_time_sec, end_time_sec, distance):
    time_diff_hours =((end_time_sec - start_time_sec)/ 360)
    if time_diff_hours == 0:
        return 0
    return  distance / time_diff_hours

def calculate_latency(submit_time_ns):
    return (time.time_ns() - submit_time_ns)  / 1000000


estimate_pi_udf = udf(estimate_pi, IntegerType())

average_speed_udf = udf(calculate_average_speed_mph, FloatType())

calculate_latency_udf = udf(calculate_latency, IntegerType())


df_with_udfs = json_df.withColumn("latency", calculate_latency_udf(col("time_ns"))).withColumn("average_speed", average_speed_udf(col("tpep_pickup_datetime"), col("tpep_dropoff_datetime"), col("trip_distance"))).withColumn("pi_estimate", estimate_pi_udf(col("sparkpi")))


# Print to console
query = df_with_udfs.writeStream \
    .outputMode("append") \
    .format("console") \
    .start()

query.awaitTermination()
