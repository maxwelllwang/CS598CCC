import json
import time
import signal
import resource
import pandas as pd
from custom_kafka_producer import CustomKafkaProducer
import pyarrow.parquet as pq
import sys


def main():
    nyc_taxi_topic = 'nyc-taxi'
    prod = CustomKafkaProducer(topic_names=[nyc_taxi_topic])
    parquet_file = pq.ParquetFile('yellow_tripdata_2023-09.parquet')

    start = time.time()
    count = 0
    for batch in parquet_file.iter_batches():
        
        for index, r in batch.to_pandas().iterrows():


            say = {
                'time_ns': int(time.time_ns()),
                'tpep_pickup_datetime': str(r['tpep_pickup_datetime']),
                'tpep_dropoff_datetime': str(r['tpep_dropoff_datetime']),
                'passenger_count': int(r['passenger_count']),
                'trip_distance': float(r['trip_distance']),
                'fare_amount': float(r['fare_amount']),
                'total_amount': float(r['total_amount'])
            }
            jo = json.dumps(say)

            prod.write_topic(nyc_taxi_topic, jo)


            count += 1

            percent_complete = count / 2846722
            sys.stdout.write(f'\rProgress: {percent_complete:.2f}%, Rate: {int(count/(time.time()-start))} per second' )
            sys.stdout.flush()

    end = time.time()
    print("total time passed:", end - start)


if __name__ == "__main__":
    #  set_max_runtime(60)
    main()
