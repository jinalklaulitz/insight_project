# Tw0rds! Develop Insight! With Twitch Slangs and Lingos!
# Kafka

## Table of Contents
1. [Introduction](README.md#introduction)
1. [System setup](README.md#System-setup)

## Introduction  
Kafka is used to ingest files from the Twitch API to the Spark, where Spark receives it as a stream and creates the raw Delta Lake tables. For this, i only use a producer with a single kafka topic 'Twitchchat'.

## System setup
The Kafka cluster is 2 node M4L cluster, seperate zookeeper and kafka broker.

