# EMIS-Assessment-local

## Description

- The solution which I provided is serverless and based on complete AWS services. This solution doesn't needed docker containarized.
- To check the functionality of spark script, I have provided the local setup with docker compose.

## Setup
 
- Install docker desktop if windows or docker from official website for other OS.
- Once the docker engine has been up and running, run the below command from file path where `docker-compose.yml` file located:

``` 
docker-compose up -d
```

- You can check the running containers by using `docker ps`.
- Now, open the below two UI for monitoring:
```
Hadoop UI - http://localhost:9870

Spark UI - http://localhost:8080
```
- Copy the patient file from github repo (https://github.com/emisgroup/exa-data-eng-assessment/tree/main/data)
and paste it in namenode:
```
docker cp Aaron697_Dickens475_8c95253e-8ee8-9ae8-6d40-021d702dc78e.json <namenode-container-id>:/data/Aaron697_Dickens475_8c95253e-8ee8-9ae8-6d40-021d702dc78e.json
```
- Open the namenode in bash shell and move the json file into HDFS.
```
docker exec -it <namenode-container-id> bash
```
```
hdfs dfs -mkdir /data
hdfs dfs -mkdir /data/patients
cd /data
hdfs dfs -put Aaron697_Dickens475_8c95253e-8ee8-9ae8-6d40-021d702dc78e.json /data/patients/Aaron697_Dickens475_8c95253e-8ee8-9ae8-6d40-021d702dc78e.json
```
- Download mysql-connector jar file from https://dev.mysql.com/downloads/connector/j/ . Select OS as "Platform Independent".
- Copy the spark script and mysql-connector jar file into spark master container
```
docker ps sparkScript.py <spark-master-container-id>:/opt/sparkScript.py
```
```
docker ps mysql-connector-j-9.0.1.jar <spark-master-container-id>:/opt/mysql-connector-java.jar
```
- Open spark master in bash shell and execute spark submit to execute the program
```
spark-submit \
  --master spark://<spark-master-container-id>:7077 \
  --jars /opt/mysql-connector-java.jar \
  /opt/sparkScript.py
```
- You can monitor the running jobs in Spark UI. 
- Once the job is completed, open mysql and check for the records.
```
docker exec -it mysql mysql -u spark -p testdb
```
```
show tables;
SELECT count(*) FROM flattened_data;
SELECT * FROM flattened_data limit 10;
```
