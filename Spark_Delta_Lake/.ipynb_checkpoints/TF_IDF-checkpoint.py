##################################################################################
# Tw0rds : Spark - Term Frequency - Iverse Document Frequency
# Author : Marvin S Mananghaya
# Created on : 19/06/2019
#
#  Input files: Extracted slangs Delta-S3 Table
#  Output file:  Messages
#  Notes:
#  How to run: spark-submit <options> TF_IDF.py
#  Libraries required:
##################################################################################

#declare libraries
import pyspark
from pyspark.sql import SQLContext
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

#declare parameters
spark = SparkSession.builder.appName('TF_IDF').getOrCreate()
sc = spark.sparkContext
path_messages = os.environ['messages']

#load messages delta lake table
slangs_ = spark.read.format("delta").load(path_messages)
#load in memory
slangs_ = slangs_.persist()
#distribute spark dataframe across clusters
slangs_ = broadcast(slangs_)

#create idf function - udf
def idf_func(df):
    import math
    return math.log10(docCount / df) 

idf_udf = udf(idf_func, FloatType())

#get term frequency
CalcTF = slangs_.groupBy("vid_id", "_slangs").agg(count("convo").alias("tf"))
#count documents, required for idf
docCount = slangs_.agg(countDistinct('vid_id')).head()[0]
#get IDF
CalcIDF = slangs_.groupBy("_slangs").agg(countDistinct("vid_id").alias("df")).withColumn('idf',idf_udf(col('df')))
#calculate TF-IDF
TF_IDF = CalcTF.join(CalcIDF, CalcTF._slangs==CalcIDF._slangs,how="left").drop(CalcIDF._slangs).withColumn("tf_idf", col("tf") * col("idf"))
#use windows functions to get top 5 terms based TF-IDF
window = Window.partitionBy(TF_IDF['vid_id']).orderBy(TF_IDF['tf_idf'].desc())
top5_remove = TF_IDF.select('*', rank().over(window).alias('rank')).filter(col('rank') <= 5)
#do a broadcast anti leftjoin (return rows that don't match with with lookup table based on top 5)
cleaned_messages = slangs_.join(broardcast(top5_remove), (slangs_.vid_id == top5_remove.vid_id) & (slangs_._slangs == top5_remove._slangs),'left_anti')
#save cleaned messages table
cleaned_messages.write.format("delta").save(path_messages)