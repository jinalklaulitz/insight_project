#!/usr/bin/python
##################################################################################
# Tw0rds : Retrieve video to determine which game metadata.py
# Author : Marvin S Mananghaya
# Created on : 16/06/2019
#
#  Input files: Videos id list (from videos Delta-S3 Table)
#  Output file: Games - Video list
#  Notes:
#  How to run: python <session> retrieve_vid_meta.py (ran using airflow's bash operator)
#  session refers to certain EC2 instance
##################################################################################


#import libraries
import time
import sys
import csv
import os
import subprocess
from twitch import TwitchClient
from multiprocessing import Pool

#define parameters
session=sys.argv[1]
input_file_list = os.environ['vid_list']
output_file_list = os.environ['game_vid_list']
client_id = os.environ['TWITCH_CLIENT{}'.format(session)]
client = TwitchClient(client_id=client_id)

with open(input_file_list, newline='', encoding='utf-8') as input_file:
    reader = csv.reader(input_file)
    for user in reader:
        vid_id_list.extend(user)

#get_game_info
def extract_game(vid_id):
    #force backoff counter
    time.sleep(1)
    channel = client.channels.get_by_id(vid_id)
    game = channel.game
    time.sleep(1)
    return game

output_file = open(output_file_list,"w")
for vid_i in vid_id_list:
    try:
        print('{},{}'.format(vid_i,extract_game(vid_i)),file=output_file)
    except:
        time.sleep(300)
        continue

output_file.close()
