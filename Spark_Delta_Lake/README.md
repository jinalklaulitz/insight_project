# Tw0rds! Develop Insight! With Twitch Slangs and Lingos!
# Spark - Delta Lake

## Table of Contents
1. [Introduction](README.md#introduction)
1. [System setup](README.md#Potential-areas-for-extensions)
   1. [System Requirements](README.md#System-components-in-detail)
   2. [Spark packages used](README.md#System-components-in-detail)
   3. [Spark Configuration](README.md#System-components-in-detail)
      1. [spark-env.sh](README.md#System-components-in-detail)
      2. [spark-defaults.conf](README.md#System-components-in-detail)

## Introduction  
Spark - Delta Lake manages the S3 data lake and performs text processing for tw0rds. Delta Lake is a new Spark package and since it's a just Spark package, in practice it works as if you're working on a Spark job.   
Spark - Delta Lake is responsible for following tasks :  
* Creation of Delta Lake tables.  
* Fields extraction from the Twitch-API generated JSON files.  
* Look-up operations of the knowledge bases.  
* Jaccardian Similarity with Levenshtein Distance.  
* Term Frequency - Inverse Document Frequency. (TF-IDF)

## System setup
The Spark - Delta Lake Cluster is composed of 9 M4xls EC2 instances, all using Ubuntu 18.04 with Python 3.7 (requirement for Twitch-API).

### System requirements
* Spark 2.4.3  
* Hadoop 2.9 (and above, atleast 2.8)
  
### Spark packages used
* io.delta:delta-core_2.12:0.1.0
* org.apache.hadoop:hadoop-aws:2.9.2
* org.apache.spark:spark-sql-kafka-0-10_2.12:2.4.3

### Spark configuration  
Spark configuration customization is based on the following tutorials:
* https://thebigan.wordpress.com/2017/10/05/garbage-collection-tuning-in-spark-part-2/
* https://code.fb.com/core-data/apache-spark-scale-a-60-tb-production-use-case/

#### Spark-env.sh
Spark_Executor_Core = 5  
Spark_Executor_Memory = 10g  
Spark_Drive_Memory = 10g  

####  spark-defaults.conf
Propery - Value  
spark.shuffle.file.buffer	2m  
spark.unsafe.sorter.spill.reader.buffer.size	2m  
spark.file.transferTo	FALSE  
spark.io.compression.lz4.blockSize 512k  
spark.shuffle.unsafe.file.output.buffer	5m  
spark.shuffle.service.index.cache.size	2048  
spark.shuffle.io.serverThreads	128  
spark.shuffle.io.backLog	8192  
spark.shuffle.registration.timeout	2m  
spark.shuffle.registration.maxAttempts	5  
spark.sql.files.maxPartitionBytes	268435456  
spark.sql.shuffle.partitions	200  
spark.hadoop.fs.s3a.impl	org.apache.hadoop.fs.s3a.S3AFileSystem  
spark.delta.logStore.class	org.apache.spark.sql.delta.storage.S3SingleDriverLogStore  
spark.executor.extraClassPath	/usr/local/spark/lib/aws-java-sdk-bundle-1.11.199.jar:/usr/local/spark/lib/hadoop-aws-2.9.2.jar  
spark.driver.extraClassPath	/usr/local/spark/lib/aws-java-sdk-bundle-1.11.199.jar:/usr/local/spark/lib/hadoop-aws-2.9.2.jar  
spark.jars.packages	com.databricks:spark-csv_2.10:1.1.0,io.delta:delta-core_2.12:0.1.0,org.apache.hadoop:hadoop-aws:2.9.2,org.apache.spark:spark-sql-kafka-0-10_2.12:2.4.3  
spark.executor.instances	8  
spark.executor.extraJavaOptions	-XX:ParallelGCThreads=4  
spark.memory.offHeap.enabled	TRUE  
spark.memory.offHeap.size	3g  
spark.executor.memory	10g  
spark.max.fetch.failures.per.stage	10  
spark.rpc.io.serverThreads	128  
spark.shuffle.service.enabled	TRUE  
spark.dynamicAllocation.enabled	TRUE  
spark.dynamicAllocation.executorIdleTimeout	2m  
spark.dynamicAllocation.minExecutors	1  
spark.dynamicAllocation.maxExecutors	7  
spark.dynamicAllocation.cachedExecutorIdleTimeout	2m  
spark.master	spark:<ip address>
