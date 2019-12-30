# Tw0rds! Develop Insight! With Twitch Slangs and Lingos!

## Table of Contents
1. [Introduction](README.md#Introduction)
1. [Motivation](README.md#Motivation)
1. [Approach](README.md#Approach)
   1. [Tokenization](README.md#Tokenization)
   1. [Urban Dictionary Lookup - English Knowledge Base Lookup](README.md#Tokenization)
   1. [Jaccardian Similarity with Levenshtein Distance](README.md#Tokenization)
   2. [Term Frequency - Inverse Document Frequency(TF-IDF)](README.md#Tokenization)
2. [Infrastructure](README.md#Infrastructure)
3. [Potential areas for extensions](README.md#Potential-areas-for-extensions)
4. System components in detail
   * [Kafka](./kafka)  
   * [Spark-Delta Lake-S3](./Spark_Delta_Lake)  
   * [Redshift](./Redshift)  
   * [Airflow and other related scripts](./Airflow)  

## Introduction  
Tw0rds is a dashboard to perform Exploratory Data Analysis based on the statistics of slangs and lingos identified from Twitch chat logs.
You can check out the [slide deck](https://docs.google.com/presentation/d/1Cnj273iIjAE0BcU6UQUZOmDtUaeUQJolR1hUgrlN-0I/edit?usp=sharing)  or [demo](http://datamlinfrabuilder.xyz)*.
*-no longer operational as of september, 2019

## Motivation
Twitch streamers generate enormous amounts of revenue from donations[[1]](https://www.cnbc.com/2016/05/13/amazons-twitch-streamers-can-make-big-bucks.html)[[2]](https://www.dexerto.com/entertainment/twitch-streamer-receives-a-record-75-000-donation-on-stream-279897) and companies are quick to notice this [[3]](https://adexchanger.com/ad-exchange-news/how-advertisers-are-using-twitch-to-reach-people-who-hate-ads/)[[4]](https://contentmarketinginstitute.com/2018/11/brands-twitch-audience/) and had asked streamers to advertise their products and services. tw0rds builds on the idea that slangs and lingos are signals/indiciators for social groupings because by definition slangs and lingos is the vocabulary used by a specific group of people, thus one can perform pattern identification using words spoken by Twitch users to tell us more about user behavior, channel engagement and category following. 

## Approach
Slang and Lingo extraction is done with a lookup on a couple of knowledge bases and a couple of algorithimic tricks to improve extraction reliability. At high level text processing is performed as follows:  
* Tokenization
* Urban Dictionary Lookup - English Knowledge Base Lookup  
* Jaccardian Similarity with Levenshtein Distance  
* Term Frequency - Inverse Document Frequency(TF-IDF)  

### Tokenization
Because my approach makes use of lookup operations, the right tokenizer can make a big difference in matching performance. Tokenization is performed using NLTK's casual tokenizer as it's the best performing tokenizer i've found, balancing with observed tokenization performance and implementation ease. NLTK's casual tokenizer is trained on a twitter corpus thus quite closest to the informal semantic structure found in conversations in twitch. I've encountered issues getting spaCy to work with Spark particularly with speed, i've originally intended to use en_core_web_lg, however much attempts with sample sentences,i've observed it performs terribly. I've also had attempted to use flair's tokenizer but it also performs terribly. As a minor point of potential extension, one can train a tokenizer (or a general language model) based on a corpus handling informal chat conversations such as twitch's. 

### Urban Dictionary Lookup - English Knowledge Base Lookup 
Slang and lingo extraction is done using [UrbanDictionary 1999-May 2016 Definitions Corpus](https://archive.org/details/UrbanDictionary1999-May2016DefinitionsCorpus). To extract anything beyond May 2016, i perform lookup using the an english knowledge base composed of:  
* [English Dictionary](https://github.com/dwyl/english-words)
* [Google’s 10,000 most frequent english words](https://github.com/first20hours/google-10000-english/blob/master/google-10000-english.txt)
* [Unix-english dictionary](https://github.com/dolph/dictionary/blob/master/unix-words)  

and simply delete matching words found in sentences. This is implemented in Spark with UDFs with set intersections and set difference. The rationale for using set operations is both driven by my assumption that within-document level (video level) frequency of slangs and lingos is not necessarily informative, users can repeatedly enter the same word multiple times, and maybe gain an understanding of "excitement" as part situational context but sentiment (as of now) is not covered by this project and it also reduces the number of operations needed to be performed as a result.

### Jaccardian Similarity with Levenshtein Distance 
To deal with words that have the same meaning but different spelling, such as Lol, lol, LOLLLL, LOLz and etc. I performed Jaccardian Similarity. This is implemented through Spark's mllib library as MinhashLSH. To improve on similarity, Levenshtein distance was added as a second point of similarity measure. This is implemented as a Spark UDF with the python library Fuzzy Wuzzy, where i make use of the partial ratio.

### Term Frequency - Inverse Document Frequency(TF-IDF) 
To remove usernames embedded in the list of extracted slangs and lingos, TF-IDF is used as slangs tend frequently show across the chat corpus.

## Infrastructure
Tw0rds is build on an infrastructure pipeline as follows:
![tw0rds architecture](./architecture.png "tw0rds architecture")
Where:
* Kafka is used to ingest json files generated by the Twitch API
* Delta Lake - S3 is the data store, Delta Lake performs basic data management of S3. 
* Spark is used to perform text processing
* Redshift is the front-end datamart
* Tableau is the dashboard visualization tool
* Airflow is the workflow management tool 

## Potential areas for extensions
Tw0rds is a result of Insight Data Science's 7 week intensive program, where we're given AWS credits and 3 weeks to create our project. Naturally given the timeline, there are a number of things could've been implemented or i had envisioned to be included given enough time to work with tw0rds.    
* Systems:
  * Realtime streaming with Delta Lake. (Implement a Lambda Architecture infrastructure)
  * Implementation with Elasticsearch, or specialized document tools/database.
* Methodologies:
  * Deploy a clustering module for user/channel/content pattern suggestions. (i would implement hierarchical clustering)
  * Train a word embedding or use a word embredding hack to look for out of dictionary words. (tw0rds staging data can assist in annotation)
* Other things to consider:
  * Word Sense Disambigation / Entity Linking - currently tw0rds' pipeline doesn't handle this issue
  * Named Entity Recognition 
