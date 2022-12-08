import json
import os
import requests
import sqlite3


API_KEY = 'f1a90036d6e899d4aedf7b4613de0cff'
SHARED_SECRET = 'a0252537fb53c36af86169f006cc1ca2'

root_url = ' http://ws.audioscrobbler.com/2.0/'

# '?method=user.gettoptracks&user=rj&api_key=YOUR_API_KEY&format=json'

'''GET REQUESTS'''
def get_requests_url(root_url):

    p = {'method': 'user.getrecenttracks', 'user': 'emmapete', 'period': '1month', 'limit': '150', 'api_key': API_KEY, 'format': 'json'}

    r = requests.get(root_url, params = p)
    data = json.loads(r.text)

    print(data)

    return data


# '''WRITE INTO JSON FILE TO CACHE'''
# def write_json_file(dict):

#     json_object = json.dumps(dict, indent = 2)

#     with open('user_most_played_tracks.json', 'w') as f:
#         f.write(json_object)



# '''READING JSON FILE'''
# def read_file(json_file):

#     f = open(json_file, 'r')

#     file = f.read()

#     f.close()

#     contents = json.loads(file)

#     print(file)
#     return file



'''GET RECENT TRACK NAMES AND ARTIST'''
def get_recent_tracks_names(file):
    recent_track_names = []
    recent_track_artists = []

    for i in range(len(file['recenttracks']['track'])):
        for track_name in file['recenttracks']['track'][i]:
            name = file['recenttracks']['track'][i]['name']
            artist = file['recenttracks']['track'][i]['artist']['#text']
            if name not in recent_track_names:
                recent_track_names.append(name)
                recent_track_artists.append(artist)

    # print(recent_track_names)
    print(recent_track_artists)
    print(recent_track_names)
    return recent_track_names,recent_track_artists



'''TUPLE CREATED'''
def make_tuple(recent_tracks_names, recent_track_artists):
    zipped_tup = zip(recent_tracks_names, recent_track_artists)
    list_of_tuples = list(zipped_tup)

    print(list_of_tuples)
    return list_of_tuples


'''OPEN DATABASE'''
def open_database(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn


'MAKING TABLE'
def make_table(tuples, cur, conn):
    cur.execute('CREATE TABLE IF NOT EXISTS User_Data (user_top_track_id PRIMARY KEY, user_top_track_name TEXT, user_top_track_artist TEXT)')
    id = 0
    num = cur.execute('SELECT max(user_top_track_id) FROM User_Data').fetchone()[0]
    print(num)
    if num == None:
        num = -1
    for i in range(num+1, num+26):
        id = i
        song = tuples[i][0]
        artist = tuples[i][1]

        cur.execute('INSERT OR IGNORE INTO User_Data (user_top_track_id, user_top_track_name, user_top_track_artist) VALUES (?,?,?)', (id, song, artist))
    conn.commit()



def main():

    data = 'user_most_played_tracks.json'
    data_from_url = get_requests_url(root_url)
    # json_file = write_json_file(data_from_url)
    # file = read_file(json_file)
    recent_tracks, recent_artists = get_recent_tracks_names(data_from_url)
    # recent_artists = get_recent_tracks_artist(data_from_url)
    tuples = make_tuple(recent_tracks, recent_artists)

    cur, conn = open_database("MusicData.db")
    table = make_table(tuples, cur, conn)



# main()




