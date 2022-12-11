import unittest
import sqlite3
import json
import os
import csv

from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
from pprint import pprint

#Getting the information for all the tracks in a playlist

SPOTIPY_CLIENT_ID = "8a51523146a943bab749f4e0adda8e0d"
SPOTIPY_CLIENT_SECRET = "2d58e7944c0d421783046a26ba3c7a9a"
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

        # json_dict = json.dumps(response['items'])
        # file = open(cache_filename, "w")
        # file.write(json_dict)
        # file.close()
        return response['items']
#GETTING SONG TITLES
def get_song_names(playlist, cache_filename):
    # print(playlist)
    song_list = []
    
    for song in playlist:
        sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET))
        song_id = song["track"]["id"]
        urn = f'spotify:track:{song_id}'
        track = sp.track(urn)
        song_list.append(track)
    # pprint(song_list)[0][0]

    json_dict = json.dumps(song_list)
    file = open(cache_filename, "w")
    file.write(json_dict)
    file.close()

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
#Databasing
def open_database(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn
def make_list_tups(s_lst, a_lst, l_lst):
    zipped = zip(s_lst, a_lst, l_lst)
    list_of_tups = list(zipped)
    return list_of_tups
def make_len_table_25(tup_list, cur, conn):
    cur.execute("CREATE TABLE IF NOT EXISTS Durations (id PRIMARY KEY, song TEXT UNIQUE, duration FLOAT)")
    id_num = 0
    num = cur.execute("SELECT max(id) FROM Durations").fetchone()[0]
    print(num)
#(song title, artist, song length)
    if num == None:
        num = -1
    for i in range(num+1, num+26):
        id_num = i
        song = tup_list[i][0]
        duration = tup_list[i][2]
        
        cur.execute("INSERT OR IGNORE INTO Durations (id,duration) VALUES (?,?)",(id_num,duration))
    conn.commit()
def make_artist_table_25(tup_list, cur, conn):
    cur.execute("CREATE TABLE IF NOT EXISTS Artists (id PRIMARY KEY, artist TEXT)")
    id_num = 0
    num = cur.execute("SELECT max(id) FROM Artists").fetchone()[0]
    print(num)
#(song title, artist, song length)
    if num == None:
        num = -1
    for i in range(num+1, num+26):
        id_num = i
        artist = tup_list[i][1]
        
        cur.execute("INSERT OR IGNORE INTO Artists (id,artist) VALUES (?,?)",(id_num,artist))
    conn.commit()



#Main
def main():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    cache_filename = dir_path + '/' + "cache_songs.json"

    playlist_songs = get_playlist_tracks("7fwWgXdN6zozUaNLJKK07D")
    print("finish function 1")
    song_names = get_song_names(playlist_songs, cache_filename)
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

    make_len_table_25(tup_list, cur, conn)
    print("finish function 7")
    make_artist_table_25(tup_list, cur, conn)
    print("finish function 8")

# main()