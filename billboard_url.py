
from xml.sax import parseString  
from bs4 import BeautifulSoup
import re
import os
import csv
import unittest 

# GOAL: rank, song name

#getting song titles
def get_songtitles(html_file):
    #open the file 
    file = open(html_file)
    soup = BeautifulSoup(file, 'html.parser')
    file.close()

    #empty lists
    song_titles = []

    #find the titles
    title_tag = soup.find_all('h3',class_ = "c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 lrv-u-font-size-18@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-330 u-max-width-230@tablet-only") 
    for song_title in title_tag:
        title = song_title.text.strip()
        song_titles.append(title)
    print(song_titles)


#getting song ranks/ids
def get_songranks(html_file):
        #open the file 
    file = open(html_file)
    soup = BeautifulSoup(file, 'html.parser')
    file.close()

    #empty lists
    rank_id = []

    #find the ranks
    rank_tag = soup.find_all('span',class_ = "u-letter-spacing-0080@tablet")
    # print(rank_tag)
    for rank in rank_tag:
        rank = rank.text.strip()
        rank_id.append(rank)
    print(rank_id)


#main
if __name__ == '__main__':
    get_songtitles("billboard_hot100.html")
    get_songranks("billboard_hot100.html")
    # database =