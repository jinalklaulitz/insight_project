#!/bin/bash

for i in {1..9}
do
    F_CNT=$((i-1))
    CMD='"tmux new-session python3.7 chatscrapper.py '+$F_CNT+'"'
    #echo $TEST
    peg sshcmd-node spark-cluster $i $CMD
done
