#!/usr/bin/python
##################################################################################
# Tw0rds : Scrape twitch metadata and chatlogs
# Author : Marvin S Mananghaya
# Created on : 13/06/2019
#
#  Input files: userlist
#  Output file: json files
#  Notes:
#  How to run: python chatscrapper.py <session> <extract_date>  (ran using airflow's bash operator)
##################################################################################

#import libraries
import time
import sys
import csv
import os
import subprocess
from multiprocessing import Pool

#define parameters
session=sys.argv[1]
extract_date = sys.argv[2]
input_file_list = os.environ['twitch_user_list{}'.format(extract_date)]
client = os.environ['TWITCH_CLIENT{}'.format(session)]

userlist = list()

with open(input_file_list, newline='', encoding='utf-8') as input_file:
    #skips first line; skips csv header row
    reader = csv.reader(input_file)
    next(reader, None)
    for user in reader:
        if user[1]!=session:
            continue
        else:
            userlist.append(user[0])

#tcd --channel <channel> --format json --timezone America/New_York

def tcd_bash(channel):
    try:
        bashCommand = "tcd --client-id {} --channel {} --format json --timezone America/New_York --output /home/ubuntu/twitchjson/{}".format(client,channel,extract_date)
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
    except:
        time.sleep(1200)
        bashCommand = "tcd --client-id {} --channel {} --format json --timezone America/New_York --output /home/ubuntu/twitchjson/{}".format(client,channel,extract_date)
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()

#perform parallel processing 
p = Pool(2)
p.map(tcd_bash,userlist)