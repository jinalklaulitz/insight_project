#!/bin/sh

while :
    do
        eval "aws s3 sync ~/twitchjson/. s3://$bucket"
  	sleep 18000
done
