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

    iterations_per_second = 6000 # this number means nothing, just adjust it up or down until you get the rate you want
    desired_interval = 1.0 / iterations_per_second

    for batch in parquet_file.iter_batches():
        
        for index, r in batch.to_pandas().iterrows():
            loop_start_time = time.time()

            say = {
                'time_ns': float(time.time_ns()),
                'tpep_pickup_datetime': float(r['tpep_pickup_datetime'].timestamp()),
                'tpep_dropoff_datetime': float(r['tpep_dropoff_datetime'].timestamp()),
                'passenger_count': int(r['passenger_count']),
                'trip_distance': float(r['trip_distance']),
                'fare_amount': float(r['fare_amount']),
                'total_amount': float(r['total_amount']),
                'sparkpi': int(100000),
            }
            jo = json.dumps(say)
            prod.write_topic(nyc_taxi_topic, jo)


            count += 1

            loop_end_time = time.time()
            elapsed = loop_end_time - loop_start_time
            sleep_time = max(desired_interval - elapsed, 0)
            time.sleep(sleep_time)

            percent_complete = count / 2846722
            sys.stdout.write(f'\rProgress: {percent_complete:.2f}%, Rate: {int(count/(time.time()-start))} per second' )
            sys.stdout.flush()

            

    end = time.time()
    print("total time passed:", end - start)


if __name__ == "__main__":
    #  set_max_runtime(60)
    main()
