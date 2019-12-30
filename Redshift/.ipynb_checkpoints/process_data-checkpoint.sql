/*
##################################################################################
# Tw0rds : Redshift -  Process tables
# Author : Marvin S Mananghaya
# Created on : 18/06/2019
##################################################################################
*/

/*game level*/
select game,count(slangs) as count_wurds from test_games_level group by game order by count_wurds desc;

select game,count(distinct slangs) as count_wurds from test_games_level group by game order by count_wurds desc;

/*channel level*/
select channel_id,count(slangs) as count_wurds from test_games_level group by channel_id order by count_wurds desc;

select b.channel_id,b.username, sum(a.count_wurds) as cnt_wurds
from (select vid_id,count(distinct slangs) as count_wurds from test_games_level group by vid_id order by count_wurds desc) as a left JOIN
dist_channels as b 
on a.vid_id=b.vid_id
group by b.channel_id,b.username
order by cnt_wurds desc
;

create table dist_slangs as 
select distinct slangs 
from spectrum.messages
;

CREATE TABLE messages_games_unique as
SELECT distinct b.game,count(a.vid_id) as count_vids
FROM SPECTRUM.messages as a join spectrum.games as b
ON A.channel_id=B.vid_id
where slangs in 
				(
				select slangs from
					(
					select slangs,count(channel_id) as channel_count
					from channel_slangs 
					where slang_len>2 
					group by slangs
					having channel_count = 1
					order by channel_count desc
					)
				)
GROUP BY b.game
;

create table channel_game as 
select a.*,b.game
from spectrum.video as a left join spectrum.games as b
on a.channel_id=b.vid_id
;

create table agg_game_views as 
select game,sum(view_count) as views_count
from channel_game
group by game
order by views_count desc
;