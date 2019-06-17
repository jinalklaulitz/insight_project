#!/bin/bash

for i in {1..10}
do
    peg scp from-local spark-cluster $i /home/jinalklaulitz/Documents/Insight/chatscrapper.py .
done
