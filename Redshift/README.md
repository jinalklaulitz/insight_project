# Tw0rds! Develop Insight! With Twitch Slangs and Lingos!
# Redshift

## Table of Contents
1. [Introduction](README.md#introduction)
1. [System setup](README.md#Potential-areas-for-extensions)
   1. [System Requirements](README.md#System-components-in-detail)
   2. [Spark packages used](README.md#System-components-in-detail)
   3. [Spark Configuration](README.md#System-components-in-detail)
      1. [spark-env.sh](README.md#System-components-in-detail)
      2. [spark-defaults.conf](README.md#System-components-in-detail)

## Introduction  
Redshift is Tw0rds' datamart, where Tableau queries from. In particular, i make use of Redshift Spectrum to query Delta Lake tables since Delta Lake tables are Parquet-Snappy under the hood and . 
Redshift tasks are divided :  
* Source to Staging
  *  
* Staging 
  * Creation of dimension tables
    * 
  * Creation of fact table
    * 
* Star Schema

## System setup
The Redshift cluster is a 2-node dc2.large cluster.

