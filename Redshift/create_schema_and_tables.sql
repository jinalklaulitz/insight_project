/*
##################################################################################
# Tw0rds : Redshift -  Create Schema and tables
# Author : Marvin S Mananghaya
# Created on : 18/06/2019
# Notes: relies on redshift spectrum to load external tables (s3; parquet snappy aka delta tables) to redshift
##################################################################################
*/

create external schema spectrum 
from data catalog 
database /*<removed for security purposes>*/ 
iam_role /*<removed for security purposes>*/
create external database if not exists;


CREATE EXTERNAL TABLE spectrum.video(
created_at VARCHAR(200),
duration VARCHAR(200),
url VARCHAR(200),
channel_id VARCHAR(200),
channel VARCHAR(200),
view_count BIGINT,
vid_id VARCHAR(200),
title VARCHAR(200))
STORED AS PARQUET
location /*<removed for security purposes>*/
TABLE PROPERTIES ('compression_type'='snappy')
;

CREATE EXTERNAL TABLE spectrum.users(
bio VARCHAR(200),
username VARCHAR(200),
user_id VARCHAR(200),
type VARCHAR(200),
channel_id VARCHAR(200),
vid_id VARCHAR(200))
STORED AS PARQUET
location /*<removed for security purposes>*/
TABLE PROPERTIES ('compression_type'='snappy')
;

CREATE EXTERNAL TABLE spectrum.channels(
username VARCHAR(200),
channel_id VARCHAR(200),
vid_id VARCHAR(200))
STORED AS PARQUET
location /*<removed for security purposes>*/
TABLE PROPERTIES ('compression_type'='snappy')
;

CREATE EXTERNAL TABLE spectrum.games(
vid_id VARCHAR(200),
game  VARCHAR(200))
STORED AS PARQUET
location /*<removed for security purposes>*/
TABLE PROPERTIES ('compression_type'='snappy')
;

CREATE EXTERNAL TABLE spectrum.messages(
username VARCHAR(200),
channel_id VARCHAR(200),
vid_id VARCHAR(200),
user_id VARCHAR(200),
slangs VARCHAR(200))
STORED AS PARQUET
location /*<removed for security purposes>*/
TABLE PROPERTIES ('compression_type'='snappy')
;

create table english_list(
english_words VARCHAR(200))

copy english_list
from /*<removed for security purposes>*/
IAM_ROLE /*<removed for security purposes>*/
IGNOREHEADER 1
;