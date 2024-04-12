from flask import Blueprint, render_template, jsonify, abort,session
import sqlite3
from routes.user_home import get_songs

user_playlists_bp = Blueprint('user_playlists', __name__, url_prefix='/user_playlists')


@user_playlists_bp.route('/all_playlists')
def get_all_playlists_songs():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    user_id = session.get('user_id')
    cursor.execute('''
        select id, name
        from playlist
        where user_id = ?;
    ''', (user_id,))
    

    playlists = cursor.fetchall()
    all_playlist = get_playlist()
    conn.close()
   

    return render_template('user_home/all_playlists.html', playlists=playlists,all_playlist=all_playlist)

def get_playlist():
    con = sqlite3.connect('database.db')
    cursor = con.cursor()
    cursor.execute("select  * FROM playlist")
    playlist = cursor.fetchall()
    con.close()
    
    return playlist



    



@user_playlists_bp.route('/<int:playlist_id>')
def get_playlist_songs(playlist_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT songs.id, songs.title, songs.rating, songs.artist, songs.lyrics
        FROM songs
        INNER JOIN playlist_song ON songs.id = playlist_song.song_id
        WHERE playlist_song.playlist_id = ?
    ''', (playlist_id,))

    songs = cursor.fetchall()
    
        
    conn.close()
    return render_template('user_home/playlists.html', playlist_songs=songs, playlist_id=playlist_id)

