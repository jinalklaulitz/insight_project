##################################################################################
# Tw0rds : Spark - generate_vid_list.py
# Author : Marvin S Mananghaya
# Created on : 17/06/2019
#
#  Input files: Videos Delta-S3 Table
#  Output file: Videos id list
#  Notes:
#  How to run: spark-submit <options> generate_vid_list.py
#  used to reextract game categories of video (metadata on category is not included in input json file; limitation of API)
##################################################################################

#load libaries
import pyspark
from pyspark.sql import SQLContext
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

#declare parameters
spark = SparkSession.builder.appName('generate_vid_list').getOrCreate()
sc = spark.sparkContext

#parameters
path_videos = os.environ['videos']
path_videos_list = os.environ['vid_list']

#load videos delta_table
videos = spark.sql("CREATE TABLE video USING DELTA LOCATION '{}'".format(path_videos))

#select distinct video ids *channel id here refers to specific video
list_vids = spark.sql('select distinct channel_id from video').toPandas()

#generate videos list file
output_file = open(path_videos_list,"w")
for vid in list_vids['channel_id'].tolist():
    print('{}'.format(vid),file=output_file)
output_file.close()