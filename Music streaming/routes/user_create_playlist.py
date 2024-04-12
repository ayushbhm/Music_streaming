from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import sqlite3
from routes.user_home import get_songs

user_create_playlists_bp = Blueprint('user_create_playlists', __name__, url_prefix='/user_create_playlists')

# ... (existing routes)
@user_create_playlists_bp.route('/create_playlist_page')
def create_playlist_page():
    songs = get_songs()
    return render_template('/user_home/create_playlist.html',songs=songs)
                         
                         
                         
@user_create_playlists_bp.route('/create_playlist', methods=['GET', 'POST'])
def create_playlist():
    if request.method == 'POST':
        # Get selected songs and playlist name from the form
        selected_songs = request.form.getlist('selected_songs')
        playlist_name = request.form.get('playlist_name')

        # Get the user ID from the session
        user_id = session.get('user_id')

        if user_id is None:
            flash('User not logged in. Please log in to create a playlist.', 'error')
            return redirect(url_for('auth.user_login'))

        # Insert the new playlist into the database with the user's ID
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute('INSERT INTO playlist (name, user_id) VALUES (?, ?)', (playlist_name, user_id))
        playlist_id = cursor.lastrowid  # Get the ID of the newly inserted playlist

        # Insert selected songs into the playlist_song table
        for song_id in selected_songs:
            cursor.execute('INSERT INTO playlist_song (playlist_id, song_id) VALUES (?, ?)', (playlist_id, song_id))

        conn.commit()
        conn.close()

        flash('Playlist created successfully!', 'success')
        return "successful"


    # Fetch all songs for display on the create playlist page
    songs = get_songs()

    return render_template('user_home/create_playlist.html', songs=songs)
