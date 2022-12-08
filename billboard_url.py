
from xml.sax import parseString  
from bs4 import BeautifulSoup
import re
import os
import csv
import unittest 
import sqlite3


# GOAL: rank, song name

#getting song titles
def get_songtitles(html_file):
    #open the file 
    file = open(html_file)
    soup = BeautifulSoup(file, 'html.parser')
    file.close()

    #empty lists
    song_titles = []

    #find anti-hero
    antihero_tag = soup.find_all('h3', class_ = "c-title  a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 u-font-size-23@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-245 u-max-width-230@tablet-only u-letter-spacing-0028@tablet") 
    print(antihero_tag)
    for song in antihero_tag:
        # print(song)
        title = song.text.strip()
        song_titles.append(title)
    # print(song_titles)

    #find the titles
    title_tag = soup.find_all('h3',class_ = "c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 lrv-u-font-size-18@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-330 u-max-width-230@tablet-only") 
    # print(title_tag)
    for song_title in title_tag:
        title = song_title.text.strip()
        song_titles.append(title)
    # print(song_titles)
    return song_titles


#getting song ranks/ids
def get_songranks(html_file):
        #open the file 
    file = open(html_file)
    soup = BeautifulSoup(file, 'html.parser')
    file.close()

    #empty lists
    rank_ids = []

    #find the ranks
    rank_tag = soup.find_all('span',class_ = "u-letter-spacing-0080@tablet")
    # print(rank_tag)
    for rank in rank_tag:
        rank = rank.text.strip()
        rank_ids.append(rank)
    # print(rank_ids)
    return rank_ids

#making tuples
def make_tuple(song_titles, rank_ids):
    zipped_tup = zip(song_titles, rank_ids)
    # print(zipped_tup)
    tup_list = list(zipped_tup)
    # print(tup_list)
    return tup_list


# # opening database
# def open_database(db_name):
#     path = os.path.dirname(os.path.abspath(__file__))
#     conn = sqlite3.connect(path+'/'+db_name)
#     cur = conn.cursor()
#     return cur, conn

# # making the table
# def make_billboard_table(cur, conn):
#     cur.execute("DROP TABLE IF EXISTS Billboard_Data")
#     cur.execute("CREATE TABLE \"Billboard_Data\"(\"song_id\" INTEGER PRIMARY KEY, \"song_title\" TEXT, \"song_rank\" NUMBER)")
    

#main
if __name__ == '__main__':
    song_titles = get_songtitles("billboard_hot100.html")
    rank_ids = get_songranks("billboard_hot100.html")
    tuples = make_tuple(song_titles, rank_ids) 