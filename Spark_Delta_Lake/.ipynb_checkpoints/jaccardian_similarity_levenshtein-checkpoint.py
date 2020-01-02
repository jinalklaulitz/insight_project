##################################################################################
# Tw0rds : Spark - Jaccardian Similarity x Levenshtein.py
# Author : Marvin S Mananghaya
# Created on : 18/06/2019
#
#  Input files: Extracted slangs Delta-S3 Table
#  Output file:  Slang Similarity Lookup Table
#  Notes:
#  Jaccardian Similarity Threshold set at 15% from perfect match (or similarity>85%)
#  Fuzzy Wuzzy Levenshtein Distance set at similarity>85%
#  How to run: spark-submit <options> jaccardian_similarity_levenshtein.py
#  Libraries required:
#  fuzzy wuzzy
##################################################################################

#declare libraries
import pyspark
from pyspark.sql import SQLContext
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.ml.feature import FeatureHasher
from pyspark.ml.feature import CountVectorizer
from pyspark.ml.feature import MinHashLSH
from fuzzywuzzy import fuzz
import os

#declare parameters
spark = SparkSession.builder.appName('Jacc_Lev').getOrCreate()
sc = spark.sparkContext
path_messages = os.environ['messages']
path_slangs_lookup = os.environ['slangs_lookup']

#load messages delta lake table
slangs_ = spark.read.format("delta").load(path_messages)
#load in memory
slangs_ = slangs_.persist()
#distribute spark dataframe across clusters
slangs_ = broadcast(slangs_)

# define function and udf for lower string
def lower_tokens(x):
    return list(x.lower())

lower_tokens_udf = udf(lower_tokens, ArrayType(StringType()))

#define fuzzy wuzzy function
def fuzzy_wuzzy(x,y):
    return fuzz.partial_ratio(x,y)

fuzzy_wuzzy_udf = udf(fuzzy_wuzzy, IntegerType())

#create distinct list of slangs
dist_slangs = slangs_.selectExpr("slangs").dropna().dropDuplicates().withColumn("id", monotonically_increasing_id()).withColumn( 'slangs_lower', lower_tokens_udf(col('slangs')))

#define model pipeline
#regex tokenizer to split into characters
#featurize characters - index them
#perform MinHashLSH - jaccardian similarity
model = Pipeline(stages=[
    RegexTokenizer(pattern="", inputCol="slangs_lower", outputCol="tokens", minTokenLength=1),
    CountVectorizer(inputCol="tokens", outputCol="features"),
    MinHashLSH(inputCol="features", outputCol="hashValues",numHashTables=20)]).fit(dist_slangs)

#actually perform the transformation
dist_slangs_hashed = model.transform(dist_slangs)

#perform similarity join; threshold set at 85% similarity, 15% refers to distance away from perfect match
self_join = model.stages[-1].approxSimilarityJoin(dist_slangs_hashed, dist_slangs_hashed, 0.15, distCol="JaccardDistance")\
    .select(col("datasetA.slangs").alias("slangsA"),
            col("datasetB.slangs").alias("slangsB"),
            col("JaccardDistance"))


#include levenshtein distance based on fuzzy distance, threshold set at above 80% similarity
self_join = self_join.withColumn( 'LeviDistance', levenshtein(col('slangsA'),col('slangsB'))).withColumn( 'FuzzyDistance', fuzzy_wuzzy_udf(col('slangsA'),col('slangsB')))\
.where(col('FuzzyDistance')>85) 

#save lookup table for look-up operation
self_join.write.format("delta").save(path_slangs_lookup)