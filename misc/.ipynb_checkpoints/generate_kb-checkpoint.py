##################################################################################
# Tw0rds : Generate Knowledge Base - urban dictionary
# Author : Marvin S Mananghaya
# Created on : 10/06/2019
#
#  Input files: slang list from urban dictionary
#  Output file: urban dictionary knowledge base
#  Notes:
#  How to run: python generate_kb.py
##################################################################################

#load libaries
import pandas as pd

#parameters
raw_urban_dict = os.environ['raw_urban_dict']
urban_dict = os.environ['urban_dict']

#load raw file
urban_list = pd.read_csv(raw_urban_dict,error_bad_lines=False,low_memory=False,warn_bad_lines=False)
#subset and removing words with missing votes
urban_list = urban_list[['word','up_votes','down_votes']].dropna()
#get only votes that are numeric; data is dirty!
urban_list = urban_list[urban_list.up_votes.apply(lambda x: x.isnumeric())]
urban_list = urban_list[urban_list.down_votes.apply(lambda x: x.isnumeric())]
#generate composite score by substracting downvotes with upvotes
urban_list['composite'] = urban_list['up_votes'].astype('int64') - urban_list['down_votes'].astype('int64')
#get only positive votes, subset to word and remove duplicate words then turn into list, perform set difference on english dictionary and urban dictionary
diff_list = list(set(urban_list[urban_list.composite>0][['word']].drop_duplicates().word.to_list()) - set(eng_list))

output_file = open(urban_dict,"w")
for wurd in diff_list:
    print('{}'.format(wurd),file=output_file)
output_file.close()