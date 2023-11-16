import json
import time
import signal
import resource
import pandas as pd
from kafkaex import Producer


def time_exceeded(signo, frame):
    raise SystemExit(1)


def set_max_runtime(seconds):
    # setting up the resource limit
    soft, hard = resource.getrlimit(resource.RLIMIT_CPU)
    resource.setrlimit(resource.RLIMIT_CPU, (seconds, hard))
    signal.signal(signal.SIGXCPU, time_exceeded)


def main():
    prod = Producer()
    # df = pd.read_parquet("yellow_tripdata_2023-09.parquet")
    df = pd.read_csv("yellow_tripdata_2023-09.csv", dtype="str")
    res = df.to_json(orient="records")
    start = time.time()
    for r in json.loads(res):
        say = {
            'time_ns': time.time_ns(),
            'tpep_pickup_datetime': r['tpep_pickup_datetime'],
            'tpep_dropoff_datetime': r['tpep_dropoff_datetime'],
            'passenger_count': r['passenger_count'],
            'trip_distance': r['trip_distance'],
            'fare_amount': r['fare_amount'],
            'total_amount': r['total_amount']
        }
        jo = json.dumps(say)

        prod.run('nyc-taxi', jo)

    end = time.time()
    print("total time passed:", end - start)


if __name__ == "__main__":
    #  set_max_runtime(60)
    main()
