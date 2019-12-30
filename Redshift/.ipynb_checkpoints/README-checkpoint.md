# Tw0rds! Develop Insight! With Twitch Slangs and Lingos!
# Redshift

## Table of Contents
1. [Introduction](README.md#introduction)
1. [System setup](README.md#System-setup)

## Introduction  
Redshift is Tw0rds' datamart, where Tableau queries from. In particular, i make use of Redshift Spectrum to query Delta Lake tables since Delta Lake tables are Parquet-Snappy under the hood and this externally loads the files. Here are the SQL files used to create the schema and redshift tables, as well as perform aggregations needed for tableau

## System setup
The Redshift cluster is a 2-node dc2.large cluster.

