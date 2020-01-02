#!/usr/bin/python
##################################################################################
# Tw0rds : Airflow - automation
# Author : Marvin S Mananghaya
# Created on : 1/07/2019
#
# How to run: go to airflow's UI 
##################################################################################

#import libraries
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import timedelta, datetime
import datetime as dt
import os

#define parameters
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2019, 7, 1),
    'email': ['airflowjobber@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 99,
    'retry_delay': timedelta(minutes=5)
}
extract_date = time_format = dt.datetime.now().strftime('%Y-%m-%d')
dag = DAG('tw0rds', default_args=default_args, schedule_interval='0 0 * * *', catchup=False)
host =#<removed for security reasons>
user ='ubuntu'
srcDir = os.environ['default_twitch']
session= range(1,10)

#invoke twitch API
for i in session:
    downloadData= BashOperator(
        task_id='get-new-twitch',
        bash_command='python ' + srcDir + '/{} {} chatscrapper.py'.format(i,extract_date),
        dag=dag)

#move to s3 - depreciated function
#move2bucket= BashOperator(
#    task_id='ec2Tos3',
#    bash_command='bash + srcDir + 'jsonec2s3.sh' ,
#    dag=dag)
# downloadData.set_downstream(move2bucket)

#generate today's userlist
downloadData= BashOperator(
    task_id='generate-todays-userlist',
    bash_command='python ' + srcDir + '/generate_todays_userlist.py',
    dag=dag)
 
#retrieve video metadata
for i in session:
    downloadData= BashOperator(
        task_id='retrieve-vid-metadata',
        bash_command='python ' + srcDir + '/{} retrieve_vid_meta.py'.format(i),
        dag=dag)
    