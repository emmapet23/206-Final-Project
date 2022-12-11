import unittest
import sqlite3
import json
import os
import csv

import plotly.graph_objects as go
import plotly.express as px

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

    conn.commit()

    return same_count

def pie_chart(percent):
    label_list = ["User's Recent Songs", "Billboard Hot 100 Songs"]
    other_num = 100 - percent
    value_list = [percent, other_num]

    fig = go.Figure(data=[go.Pie(labels=label_list, values=value_list)])
    fig.show()

    return percent

def vis2_get_longest_songs(database_name, cur, conn):
    conn = sqlite3.connect(database_name)
    cur = conn.cursor()

    sorted_lengths = sorted(cur.execute("SELECT Billboard_Data.song_title, Durations.duration FROM Billboard_Data \
        JOIN Durations ON Billboard_Data.song_id = Durations.id").fetchall(), key = lambda t: t[1], reverse = True)

    x_list = []
    y_list = []
    combined_lst = []



    if len(x_list)<=10 and len(y_list)<=10:
        for tup in sorted_lengths:
            song_x = tup[0]
            time_y = tup[1]
            x_list.append(song_x)
            y_list.append(time_y)
    else:
        pass
    combined_lst.append(x_list)
    combined_lst.append(y_list)

    print(combined_lst)
    return combined_lst
    

def long_bar_graph(combined_lst):
    fig = go.Figure(
        data = [go.Bar(x = combined_lst[0][0:10], y = combined_lst[1][0:10], marker_color = 'rgb(52,91,94)')],
        layout = dict(title = dict(text = 'Top 10 Longest Songs in the Billboard Hot 100 in Minutes'))
    )
    # fig = px.bar(x = combined_lst[0][0:10], y = combined_lst[1][0:10], color='rgb(52,91,94)',
    # labels=dict(x="Song Title", y="Song Length"))
    fig.show()

def vis3_get_shortest_songs(database_name, cur, conn):
    conn = sqlite3.connect(database_name)
    cur = conn.cursor()

    sorted_lengths = sorted(cur.execute("SELECT Billboard_Data.song_title, Durations.duration FROM Billboard_Data \
        JOIN Durations ON Billboard_Data.song_id = Durations.id").fetchall(), key = lambda t: t[1])

    x_list = []
    y_list = []
    combined_lst = []

    if len(x_list)<=10 and len(y_list)<=10:
        for tup in sorted_lengths:
            song_x = tup[0]
            time_y = tup[1]
            x_list.append(song_x)
            y_list.append(time_y)
    else:
        pass
    combined_lst.append(x_list)
    combined_lst.append(y_list)

    print(combined_lst)
    return combined_lst

def short_bar_graph(combined_lst):
    fig = go.Figure(
        data = [go.Bar(x = combined_lst[0][0:10], y = combined_lst[1][0:10], marker_color = 'rgb(252,148,3)')],
        layout = dict(title = dict(text = 'Top 10 Shortest Songs in the Billboard Hot 100 in Minutes'))
    )
    fig.show()

def write_data(filename, percent, long_songs, short_songs):
    file = open(filename, "w")
    file.write(str(percent/100) + "percent of our user's 100 most recently listened to songs are on the Billboard Hot 100." + "\n")
    file.write("The longest songs, in minutes, on the Billboard Hot 100 are ")
    for song in long_songs[0][0:10]:
        file.write(song + ", ")
    file.write("\n")
    file.write("The shortest songs, in minutes, on the Billboard Hot 100 are ")
    for song in short_songs[0][1:10]:
        file.write(song + ", ")
    file.write("\n")
    file.close()
    


#MAIN
def main():
    database = loading_databases()
    cur, conn = open_database('MusicData.db')
    user_num_songs = spotify_lastfm_join(cur, conn)
    visualization_one = pie_chart(user_num_songs)
    top_ten_longest = vis2_get_longest_songs('MusicData.db', cur, conn)    
    visualization_two = long_bar_graph(top_ten_longest)
    top_ten_shortest = vis3_get_shortest_songs("MusicData.db", cur, conn)
    visualization_three = short_bar_graph(top_ten_shortest)

    write_data("calculations.txt", user_num_songs, top_ten_longest, top_ten_shortest)


main()