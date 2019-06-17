/*create schema twitch*/
CREATE SCHEMA twitch;

/*create table for users*/
CREATE TABLE twitch.users (user_id serial, username varchar(50), usertype varchar(50),bio text,time_stamp timestamp);

/*create table for videos*/
CREATE TABLE twitch.videos (video_id serial, title text, created_at datetime,duration int,viewcount int,url varchar(200),game_id serial);

/*create table for games*/
CREATE TABLE twitch.games (game_id text, game_name date);

/*create table for channel*/
CREATE TABLE twitch.channel (channel_id text, channel_name date);

/*create table for messages*/
CREATE TABLE twitch.message (title text, release date, awards text[]);

/*create table for slangs*/
CREATE TABLE twitch.slangs (slang_id text, slang_name date);
