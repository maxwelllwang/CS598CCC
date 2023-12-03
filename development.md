# Development log

### Kafka Producer

### Running Kafka

* EC2 instance
  * WE ARE USING `us-east-1` for EVERYTHING
  * t2.micro in us-east-1 30gb storage cs598.pem on maxwell's computer
  * USE ec2 INSTANCE CONNECT
  * installed docker and docker compose 
  * running kafka in docker compose application
    * using docker-compose
    * t2.micro didn't have enough ram scaled up to t2.medium
  * https://github.com/conduktor/kafka-stack-docker-compose.git
    * used this as an example to setup kafka
  * 

* py-kafka producer
  * to start kafka server
    * navigate to the `CS598CCC/` repo or wherever your `docker-compose.yml` file is
    * `docker compose up -d`
    * this needs to be started for python kafka to find the kafka server
    
* Pyspark Consumer
  * `docker pull apache/spark-py`
  * `docker run -u root --rm -it --network=host -v /home/ubuntu/CS598CCC/:/opt/spark/work-dir/CS598CCC apache/spark-py /bin/bash`
	* you have to run as root or you don't have permission to download the packages you need
  * `/opt/spark/bin/spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.0 CS598CCC/pyspark-example.py`
  * 

* Producer (NYC taxi data)
  * `python3 prod.py` 

* Provisioning eks cluster
  * https://medium.com/nerd-for-tech/pyspark-spark-operator-amazon-eks-big-data-on-steroids-7d1ccedb765b
  * installing kubctl eksctl helm awscli
  * should be in /usr/local/bin for `ubuntu` user
  * setting up aws credentials using `aws configure`
  * ran `eksctl create cluster -f eks-cluster.yaml`
  * installed `k9s` please use it, its glorious
  * `aws s3 cp pyspark-example.py s3://cs598sparkjobs/` this is how sparkjobs accesses our files

* Prometheus monitoring
  * `cd prometheus-2.48.0.linux-amd64/`
  * `./prometheus --config.file=prometheus.yml`
  * open `[ec2IP]:9090` in a browser for the ui
    * check `[ec2IP]:9090/metrics`
    * query from `[ec2IP]:9090/graphs`
