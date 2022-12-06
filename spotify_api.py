import unittest
import sqlite3
import json
import os
import csv

from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
from pprint import pprint

#Getting the information for all the tracks in a playlist

SPOTIPY_CLIENT_ID = "37e1bb8ba38d41ca85ec84727b4e0a56"
SPOTIPY_CLIENT_SECRET = "913ca8aa20634351846b11dd5523cffb"
SPOTIPY_REDIRECT_URI = "https://localhost:8888/callback"


#GETTING PLAYLIST WORTH OF SONG IDS
def get_playlist_tracks(id):

    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET))

    pl_id = f'spotify:playlist:{id}'
    offset = 0

    while True:
        response = sp.playlist_items(pl_id,
                                    offset=offset,
                                    fields='items.track.id,total',
                                    additional_types=['track'])
        
        if len(response['items']) == 0:
            break
        
        # pprint(response)
        # pprint(response["items"])
        offset = offset + len(response['items'])
        # print(offset, "/", response['total'])
        return response['items']

#GETTING SONG TITLES
def get_song_names(playlist):
    # print(playlist)

    song_list = []
    
    for song in playlist:
        sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET))
        song_id = song["track"]["id"]
        urn = f'spotify:track:{song_id}'
        track = sp.track(urn)
        song_list.append(track)
    # pprint(song_list)[0][0]

    title_list = []
    for dictionary in song_list:
        song_title = dictionary["name"]
        title_list.append(song_title)
    # print(title_list)
    return title_list

#GETTING ARTISTS
def get_artists(playlist):
    song_list = []
    
    for song in playlist:
        sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET))
        song_id = song["track"]["id"]
        urn = f'spotify:track:{song_id}'
        track = sp.track(urn)
        song_list.append(track)

    artist_list = []
    for dictionary in song_list:
        artist = dictionary["artists"][0]["name"]
        artist_list.append(artist)
    # print(artist_list)
    return artist_list

#GETTING SONG LENGTHS
def get_durations(playlist):
    song_list = []
    
    for song in playlist:
        sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET))
        song_id = song["track"]["id"]
        urn = f'spotify:track:{song_id}'
        track = sp.track(urn)
        song_list.append(track)

    length_list = []
    for dictionary in song_list:
        len_s = dictionary["duration_ms"]
        len_min = round((len_s/(1000*60))%60, 2)
        length_list.append(len_min)
    # print(length_list)
    return length_list

def open_database(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

#MAKING TABLE with durations
def make_len_table(s_lst, l_lst, cur, conn):
    cur.execute("CREATE TABLE IF NOT EXISTS Durations (id PRIMARY KEY, song TEXT UNIQUE, duration FLOAT)")
    count = 0
    for i in range(len(s_lst)):
        count+=1
        song = s_lst[i]
        duration = l_lst[i]
        cur.execute("SELECT {count} (id,song,duration) FROM Spotify")
        cur.execute("INSERT OR IGNORE INTO Spotify (id,song,duration) VALUES (?,?,?)",(count,song,duration))
    conn.commit()

# for tup in list_of_tups:
#     cur.execute(INSERT values FOR list_of_tups[number:number+25])

#Making table 25 at a time
def make_list_tups(s_lst, a_lst, l_lst):
    zipped = zip(s_lst, a_lst, l_lst)
    list_of_tups = list(zipped)
    return list_of_tups

def make_len_table_25(tup_list, cur, conn):
    cur.execute("CREATE TABLE IF NOT EXISTS Durations (id PRIMARY KEY, song TEXT UNIQUE, duration FLOAT)")
    count = 0
    num = cur.execute("SELECT count(id) FROM Durations").fetchone()[0]
    print(num)

    for tup in tup_list[num:num+25]:
        count +=1
        song = tup[0]
        duration = tup[2]
        
        cur.execute("INSERT OR IGNORE INTO Durations (id,song,duration) VALUES (?,?,?)",(count,song,duration))
        conn.commit()


#Main
def main():
    playlist_songs = get_playlist_tracks("7fwWgXdN6zozUaNLJKK07D")
    print("finish function 1")
    song_names = get_song_names(playlist_songs)
    print("finish function 2")
    artist_names = get_artists(playlist_songs)
    print("finish function 3")
    lengths_songs = get_durations(playlist_songs)
    print("finish function 4")
    # write_file("music_tups.csv", song_names, artist_names, lengths_songs)

    cur, conn = open_database("MusicData.db")
    print("finish function 5")

    tup_list = make_list_tups(song_names, artist_names, lengths_songs)
    print("finish function 6")

    # make_len_table(song_names, lengths_songs, cur, conn)
    # make_artists_table(song_names, artist_names, cur, conn)

    make_len_table_25(tup_list, cur, conn)
    print("finish function 7")



main()