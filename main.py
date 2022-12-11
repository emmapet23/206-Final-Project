import unittest
import sqlite3
import json
import os
import csv

import plotly.graph_objects as go

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

    same = cur.fetchall()
    same_count = len(same)
    # percentage = (same_count/100)

    # print(same)
    # print(same_count)
    # print(percentage)
    conn.commit()

    # return percentage
    return same_count

    # shared_count = len(thing)
    # percentage = (shared_count/100)

def pie_chart(percent):
    label_list = ["User's Recent Songs", "Billboard Hot 100 Songs"]
    other_num = 100 - percent
    value_list = [percent, other_num]

    fig = go.Figure(data=[go.Pie(labels=label_list, values=value_list)])
    fig.show()

def vis2_get_longest_songs(database_name, cur, conn):
    conn = sqlite3.connect(database_name)
    cur = conn.cursor()
    # sorted_lengths = sorted(cur.execute("SELECT duration FROM Durations").fetchall(), reverse=True)

    sorted_lengths = sorted(cur.execute("SELECT Billboard_Data.song_title, Durations.duration FROM Billboard_Data \
        JOIN Durations ON Billboard_Data.song_id = Durations.id").fetchall(), key = lambda t: t[1], reverse = True)

    long_list = []
    # count = 0
    while len(long_list)<=10:
        for time in sorted_lengths:
            print(time)
        





#MAIN
def main():
    database = loading_databases()
    cur, conn = open_database('MusicData.db')
    user_num_songs = spotify_lastfm_join(cur, conn)
    
    visualization_one = pie_chart(user_num_songs)
    return visualization_one

main()