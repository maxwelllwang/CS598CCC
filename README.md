# CS598CCC
CS598 Project to test autoscaling spark jobs consuming from kafka running on Elastic Kubernetes Service. 


### Setup
## EC2 instance
* Setup using UI t2.medium in `us-east-1`
* Please SSH using the browser SSH client, 
  * maxwell has the `.pem` if you want to ssh from your terminal
* PLEASE TURN IT OFF ONCE YOU'RE DONE, if you leave it on for too long we will have to split costs
* Setting up environment
  * Install `docker` `python3-venv` `python3-pip`
  * python venv
    * `python3 -m venv myvenv`
    * `source myvenv/bin/activate`
    * `python3 -m pip instal -r requirements.txt`
* `pyspark-example` needs to be run inside of the docker image
* `prod.py` reads from `yellow_tripdata_2023-09.parquet` and uses custom-kafka-producer