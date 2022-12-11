
from xml.sax import parseString  
from bs4 import BeautifulSoup
import os
import sqlite3
import requests


# GOAL: rank, song name

# #get link
# def getLink(soup):
#     link = 'https://web.archive.org/web/20221205112648/https://www.billboard.com/charts/hot-100/'.get('href')
#     return link

#getting song titles
def get_songtitles(soup):
    #empty lists
    song_titles = []

    #find anti-hero
    antihero_tag = soup.find('h3', class_ = "c-title") 
    title = antihero_tag.text.strip()
    song_titles.append(title)

    #find the titles
    title_tag = soup.find_all('h3',class_ = "c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 lrv-u-font-size-18@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-330 u-max-width-230@tablet-only") 
    # print(title_tag)
    for song_title in title_tag:
        title = song_title.text.strip()
        song_titles.append(title)
    # print(song_titles)
    return song_titles


#getting song ranks/ids
def get_songranks(soup):
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


# get artist name
def get_artistname(soup):
    #empty lists
    artist_names = []

    #find artist name
    artist_tag = soup.find_all('span',class_ = "u-letter-spacing-0021")
    for artist in artist_tag:
        artist = artist.text.strip()
        artist_names.append(artist)
    # print(artist_names)
    return artist_names

#making tuples
def make_tuple(song_titles, rank_ids, artist_names):
    zipped_tup = zip(song_titles, rank_ids, artist_names)
    # print(zipped_tup)
    tup_list = list(zipped_tup)
    # print(tup_list)
    return tup_list


# opening database
def open_database(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

# making the table
def make_billboard_table(tuples, cur, conn):
    cur.execute("CREATE TABLE IF NOT EXISTS Billboard_Data (song_id PRIMARY KEY, song_title TEXT UNIQUE, song_rank INTEGER)")
    id_num = 0
    num = cur.execute("SELECT max(song_id) FROM Billboard_Data").fetchone()[0]
    # print(num)
#(id, song_title,rank)
    if num == None:
        num = -1
    for i in range(num+1, num+26):
        id_num = i
        song = tuples[i][0]
        rank = tuples[i][1]
        # artist_name = tuples[i][2]
        # artist_id = cur.execute('SELECT id FROM Artists WHERE artist = (?)', (artist_name,)).fetchone()[0]
        # artist_id = cur.fetchone()[0]
        # print(type(artist_id))

        # cur.execute('SELECT id FROM Types WHERE type = ?',(types[0],)) 
        # type_id = int(cur.fetchone()[0])


        #^^^ SHOULD THIS BE artist_id = cur.execute("SELECT id FROM Artists WHERE Artists.artist = (?)", (tuples[i][2], )).fetchone()[0]
        
        cur.execute("INSERT OR IGNORE INTO Billboard_Data (song_id, song_title, song_rank) VALUES (?,?,?)",(id_num, song, rank))
    conn.commit()


#main
def main():
    url = 'https://web.archive.org/web/20221205112648/https://www.billboard.com/charts/hot-100/'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    # print(type(soup))

    song_titles = get_songtitles(soup)
    rank_ids = get_songranks(soup)
    artist_names = get_artistname(soup)
    tuples = make_tuple(song_titles, rank_ids, artist_names) 

    cur, conn = open_database("MusicData.db")
    table = make_billboard_table(tuples, cur, conn)

# main() 

    # call main() 