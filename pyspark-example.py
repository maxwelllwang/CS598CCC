from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StringType, IntegerType, BooleanType
import time 


print("main start")
scala_version = '2.12'
spark_version = '3.4.0'

packages = [
    f'org.apache.spark:spark-sql-kafka-0-10_{scala_version}:{spark_version}',
    'org.apache.kafka:kafka-clients:3.2.1'
]


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

nyc_taxi_topic_name = "nyc-taxi"


jsonSchema = StructType([
    StructField("field1", StringType()),
    StructField("field2", IntegerType()),
    StructField("sparkpi", BooleanType()),
    # Add more fields based on your JSON structure
])


# Read from Kafka
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
    .option("subscribe", nyc_taxi_topic_name) \
    .load()

json_df = df.select(
    from_json(col("value").cast("string"), jsonSchema).alias("parsed_value")
)

if (json_df['sparkpi']):
    partitions = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    n = 100000 * partitions

    def f(_: int) -> float:
        x = random() * 2 - 1
        y = random() * 2 - 1
        return 1 if x ** 2 + y ** 2 <= 1 else 0

    count = spark.sparkContext.parallelize(range(1, n + 1), partitions).map(f).reduce(add)
    print("Pi is roughly %f" % (4.0 * count / n))


latency_ms = json_df['latency_ns'] + time.time_ns() * 1000000

# Select the value field and cast it to string
df = df.selectExpr("CAST(value AS STRING)")

# Print to console
query = df.writeStream \
    .outputMode("append") \
    .format("console") \
    .start()

query.awaitTermination()
