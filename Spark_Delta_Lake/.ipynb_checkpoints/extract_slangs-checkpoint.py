##################################################################################
# Tw0rds : Spark - extract_slangs.py
# Author : Marvin S Mananghaya
# Created on : 17/06/2019
#
#  Input files: Messages Delta-S3 Table
#  Output file: Extracted slangs Delta-S3 Table
#  Notes:
#  How to run: spark-submit <options> extract_slangs.py
##################################################################################

#load libaries
import pyspark
from pyspark.sql import SQLContext
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
from nltk.tokenize import TweetTokenizer

#declare parameters
spark = SparkSession.builder.appName('extract_slangs').getOrCreate()
sc = spark.sparkContext

#parameters
path_messages = os.environ['messages']
urbandict_file = os.environ['urban_dict']
english_file = os.environ['english_list']
path_extracted_slangs = os.environ['extracted_slangs']

#define functions
def file_reader(input_path):
    import csv
    list_container = list()
    with open(input_path, newline='', encoding='utf-8') as input_file:
        reader = csv.reader(input_file)
        for file_row in reader:
            list_container.extend(file_row)
    return list_container

def clean_text(text):
    import re
    #website, email pattern
    # removed for now and proper cased 
    rgx_list = [r'((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z0-9\&\.\/\?\:@\-_=#])*',r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+',r'@[a-zA-Z0-9-.]+']
    #,r'[A-Z][a-z]+']
    new_text = text
    for rgx_match in rgx_list:
        new_text = re.sub(rgx_match, '', new_text)
    return new_text

# tokenize text
def nltk_tolkenizer(x):
    from nltk.tokenize import TweetTokenizer
    tknzr = TweetTokenizer()
    return tknzr.tokenize(x)

#define udfs
def add_eng():
    return english_list.value

def add_ubdict():
    return urbandict_list.value

add_ubdict_udf = udf(add_ubdict, ArrayType(StringType()))
add_eng_udf = udf(add_eng, ArrayType(StringType()))
removeemailurl_udf = udf(clean_text, StringType())
nltk_tolkenizer_udf = udf(nltk_tolkenizer, ArrayType(StringType()))

#load knowledge bases
urbandict_list = file_reader(urbandict_file)
english_list = file_reader(english_file)

#broadcast knowledge base across cluster
urbandict_list=sc.broadcast(urbandict_list)
english_list=sc.broadcast(english_list)

#load current messages table
messages = spark.read.format("delta").load(path_messages)

#load in memory
messages.persist()
#distribute dataframe across clusters
messages = broadcast(messages)

extracted_slangs_output = messages.withColumn( 'processed', removeemailurl_udf(col('body'))).withColumn('processed', nltk_tolkenizer_udf(col('processed')))\
.withColumn('urbandict', add_ubdict_udf()).withColumn('slangs',array_intersect('processed','urbandict')).withColumn('processed',array_except('processed','urbandict'))\
.selectExpr("vid_id","username","user_id","channel_id","slangs","processed").withColumn('engdict', add_eng_udf()).withColumn('processed',array_except('processed','engdict'))\
.selectExpr("vid_id","username","user_id","channel_id","concat(slangs,processed) as _slangs")

#write extracted slangs output into delta table
extracted_slangs_output.write.format("delta").save(path_extracted_slangs)
