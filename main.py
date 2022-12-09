import unittest
import sqlite3
import json
import os
import csv

import spotify_api
import last_fm_api
import billboard_url


def loading_databases():
    spotify_api.main()
    last_fm_api.main()
    billboard_url.main()

def open_database(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor() 
    return cur, conn


def spotify_lastfm_join(cur, conn):
    cur.execute("SELECT User_Data.user_top_track_name, Billboard_Data.song_title FROM User_Data \
        INNER JOIN Billboard_Data ON User_Data.user_top_track_name = Billboard_Data.song_title")
    print(cur.fetchall())
    conn.commit()

    return cur.fetchall()

    # shared_count = len(thing)
    # percentage = (shared_count/100)


#MAIN
def main():
    database = loading_databases()
    cur, conn = open_database('MusicData.db')
    spotify_lastfm_join(cur, conn)

main()