##################################################################################
# Tw0rds : Spark - extract fields -  Kafka connection
# Author : Marvin S Mananghaya
# Created on : 17/06/2019
#
#  Input files: json files from kafka
#  Output file:  messages, videos, users, 
#  Notes:
#
#  How to run: spark-submit <options> extract_field.py <extract_date;%Y-%m-%d> ; run using airflow
##################################################################################


#load libaries
import pyspark
from pyspark.sql import SQLContext
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.streaming import StreamingContex, readStream, writeStream
from pyspark.streaming.kafka import KafkaUtils
import json
import boto3

#declare spark parameters
spark = SparkSession.builder.appName('spark_kafka').getOrCreate()
sc = spark.sparkContext
ssc = StreamingContext(sc, 60)
kafkaStream = KafkaUtils.createStream(ssc, \
     'ubuntu@10.0.0.14:2181', 'TwitchChat',2)

#parameters
extract_date = sys.argv[1]
#s3a path
path_messages = os.environ['messages']
path_videos = os.environ['videos']
path_users = os.environ['users']
kafka_broker = os.environ['broker']

#load kafka sent messages
kafka_messages = spark.readStream
            .format("kafka")
            .option("kafka.bootstrap.servers", kafka_broker)
            .option("subscribe", 'TwitchChat')
            .option("startingOffsets", "earliest")
            .option("failOnDataLoss", "false")
            .load()


#append new entries#

#append to tables - videos
kafka_messages.select("video.created_at","video.duration","video.url","video.user_id","video.user_name","video.view_count")\
  .writeStream\
  .format("delta")\
  .outputMode("append")\
  .option("checkpointLocation", "{}/_checkpoints/etl-from-json".format(path_videos))\
  .start(path_videos) 

#append to tables - messages
query_body = "comments.message" 
query_body2 = "comments.commenter" 

kafka_messages.select(col("{}.body".format(query_body)),col("{}.emoticons".format(query_body)),col("{}.name".format(query_body2))\
  .writeStream\
  .format("delta")\
  .outputMode("append")\
  .option("checkpointLocation", "{}/_checkpoints/etl-from-json".format(path_messages))\
  .start(path_messages) 

#append to tables - users
kafka_messages.select(col("comments.commenter.bio"),col("comments.commenter.name"),col("comments.commenter.type")\
  .writeStream\
  .format("delta")\
  .outputMode("append")\
  .option("checkpointLocation", "{}/_checkpoints/etl-from-json".format(users))\
  .start(path_users) 
