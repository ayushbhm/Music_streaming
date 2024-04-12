from flask import Blueprint, render_template,request,redirect,url_for,session
import sqlite3


user_home_bp = Blueprint('user_home', __name__, url_prefix='/user')


@user_home_bp.route('/')
def user_home():
    songs_list = get_songs()
    latest_songs_list = sorted(songs_list,reverse=True)
    playlist = get_playlist()
    latest_playlist=sorted(playlist,reverse=True)
    sad_songs=get_sad_songs()
    romantic_songs=get_romantic_songs()

    return render_template('/user_home/user_home.html',latest_songs_list=latest_songs_list,latest_playlist=latest_playlist,sad_songs=sad_songs,romantic_songs=romantic_songs)


def get_playlist():
    con = sqlite3.connect('database.db')
    cursor = con.cursor()
    cursor.execute("select  * FROM playlist")
    playlist = cursor.fetchall()
    con.close()
    
    return playlist


def get_songs():
    con = sqlite3.connect('database.db')
    cursor = con.cursor()
    cursor.execute("select  * FROM songs")
    songs_list = cursor.fetchall()
    con.close()
    
    return songs_list

def get_sad_songs():
    songs_list=get_songs()
    sad_songs =  [song for song in songs_list if song[5] == "sad"]
    
    return sad_songs

def get_romantic_songs():
    songs_list=get_songs()
    romantic_songs =  [song for song in songs_list if song[5] == "romantic"]
    
    return romantic_songs


