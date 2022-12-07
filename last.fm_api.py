import json
import os
import requests


API_KEY = 'f1a90036d6e899d4aedf7b4613de0cff'
SHARED_SECRET = 'a0252537fb53c36af86169f006cc1ca2'

root_url = ' http://ws.audioscrobbler.com/2.0/'

# '?method=user.gettoptracks&user=rj&api_key=YOUR_API_KEY&format=json'

'''GET REQUESTS'''
def get_requests_url(root_url):

    p = {'method': 'user.getrecenttracks', 'user': 'emmapete', 'period': '1month', 'limit': '100', 'api_key': API_KEY, 'format': 'json'}

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



'''GET RECENT TRACK NAMES'''
def get_recent_tracks_names(file):
    recent_track_names = []

    for i in range(len(file['recenttracks']['track'])):
        for track_name in file['recenttracks']['track'][i]:
            name = file['recenttracks']['track'][i]['name']
        recent_track_names.append(name)

    # print(recent_track_names)
    return recent_track_names


'''GET RECENT TRACK ARTISTS'''
def get_recent_tracks_artist(file):
    recent_track_artists = []

    for i in range(len(file['recenttracks']['track'])):
        for track_name in file['recenttracks']['track'][i]:
            artist = file['recenttracks']['track'][i]['artist']['#text']
        recent_track_artists.append(artist)

    # print(recent_track_artists)
    return recent_track_artists


'''TUPLE CREATED'''
def make_tuple(recent_tracks_names, recent_track_artists):
    zipped_tup = zip(recent_tracks_names, recent_track_artists)
    list_of_tuples = list(zipped_tup)

    print(list_of_tuples)
    return list_of_tuples



def main():

    data = 'user_most_played_tracks.json'
    data_from_url = get_requests_url(root_url)
    # json_file = write_json_file(data_from_url)
    # file = read_file(json_file)
    recent_tracks = get_recent_tracks_names(data_from_url)
    recent_artists = get_recent_tracks_artist(data_from_url)
    tuples = make_tuple(recent_tracks, recent_artists)


main()




