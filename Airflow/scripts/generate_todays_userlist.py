#!/usr/bin/python
##################################################################################
# Tw0rds : Generates today's userlist
# Author : Marvin S Mananghaya
# Created on : 13/06/2019
#
#  Input files: N/A (twitch api call)
#  Output file: userlist
#  Notes:
#  How to run: python generate_todays_userlist.py (ran using airflow's bash operator)
##################################################################################

#import libraries
import time
import sys
import csv
import os
from twitch import TwitchClient
import pprint

#define parameters
client_id = os.environ['TWITCH_API']
client = TwitchClient(client_id=client_id)

#generate a list of games
gamez = list()
i = 0
while i<10:
    gamez.extend([x.game.name for x in client.games.get_top(limit=100,offset=i)])
    i+=1

#generate a list of channels
user_list = list()

for gam_e in gamez:
    namesz = list()
    i = 0
    #get from livestreams in order to get top 100 unique channels per page per game
    while i<10:
        namesz.extend([x.channel.display_name for x in client.streams.get_live_streams(game=gam_e,language='en',limit=100,offset=i)])
        i+=1
    #append only unique channels
    user_list.extend(list(set(namesz)))

#get unique channels
user_list = list(set(user_list))

output_path="./userlist.csv"
output_file = open(output_path,"w")
header = ['username','client_id_num']
print(','.join(header),file=output_file)
i=0
for user in user_list:
    print('{},{}'.format(user,str(i)),file=output_file)
    i+=1
    if i==9:
        i=0
output_file.close()