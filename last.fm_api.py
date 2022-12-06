import json
import os
import requests








API_KEY = 'f1a90036d6e899d4aedf7b4613de0cff'
SHARED_SECRET = 'a0252537fb53c36af86169f006cc1ca2'

root_url = ' http://ws.audioscrobbler.com/2.0/'

# '?method=user.gettoptracks&user=rj&api_key=YOUR_API_KEY&format=json'



def get_requests_url(root_url):

    p = {'method': 'user.getrecenttracks', 'user': 'emmapete', 'period': '1month', 'limit': '100', 'api_key': API_KEY, 'format': 'json'}

    r = requests.get(root_url, params = p)
    data = json.loads(r.text)

    print(data)

    return data


def write_json_file(dict):

    json_object = json.dumps(dict, indent = 2)

    with open('user_most_played_tracks.json', 'w') as f:
        f.write(json_object)


def main():

    data = get_requests_url(root_url)
    file = write_json_file(data)


main()




