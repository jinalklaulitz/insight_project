#!/usr/bin/python
##################################################################################
# Tw0rds : Kafka - producer
# Author : Marvin S Mananghaya
# Created on : 19/06/2019
#
#  Input files: json files
#  Output file: <n/a> - sends files to spark
#  Notes:
#  How to run: python <extract_date;%Y-%m-%d> producer.py (ran using airflow's bash operator)
##################################################################################

#declare libraries
import json
from kafka import KafkaProducer
from os import listdir
from os.path import isfile, join

#declare parameters
extract_date = sys.argv[1]
json_path = os.environ['json_path'] + '/twitch_batch_{}'.format(extract_date)

#get current list of files
FileList = [f for f in listdir(json_path) if isfile(join(json_path, f))]

#initialize producer
producer = KafkaProducer(bootstrap_servers=['localhost:9092'])

#loop through current batch of files
for jsonFile in FileList:    
    producer.send('TwitchChat', json.dumps(jsonFile, default=json_util.default).encode('utf-8'))

