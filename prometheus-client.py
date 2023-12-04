from prometheus_client import start_http_server, Gauge
import random
import time

# Create a gauge metric
metric = Gauge('my_metric', 'Description of gauge')

# Function to generate random data for the metric
# TODO get metrics from pyspark
def generate_random_data():
    return random.uniform(0, 100)

if __name__ == '__main__':
    # Start the Prometheus HTTP server
    start_http_server(8000)

    # Main loop to update the metric
    while True:
        # Update the metric with random data
        metric.set(generate_random_data())
        time.sleep(5)
