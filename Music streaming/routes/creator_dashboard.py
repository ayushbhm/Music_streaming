from flask import Blueprint, render_template, request, redirect, url_for, flash, session,send_file
import sqlite3,io 
from werkzeug.utils import secure_filename


creator_dashboard_bp = Blueprint('creator_dashboard', __name__, url_prefix='/creator_dashboard')


@creator_dashboard_bp.route('/')
def display_creator_dashboard():
    user_id = session.get('user_id')
    user_role = get_user_role(user_id)
    if user_role == 'creator':
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("select  id, title, artist, genre, rating  from songs where creator_id = ?;", (user_id,))
        all_songs = cursor.fetchall()
        
        
        cursor.execute("select count(*) from songs where creator_id = ?;", (user_id,))
        
        num_songs = cursor.fetchone()[0]
        cursor.execute("select avg(rating) from songs where creator_id = ?;", (user_id,))
        
        avg_rating =  round(cursor.fetchone()[0],2)
        
      
        cursor.execute("select count(*) from albums where creator_id = ?;", (user_id,))
    
        num_albums = cursor.fetchone()[0]
       
        conn.close()


        print(user_id)
        return render_template('creator/creator_dashboard.html', user_role=user_role,num_songs=num_songs, avg_rating=avg_rating, num_albums=num_albums,all_songs=all_songs)
    
    
    if user_role == 'user':
        return render_template('creator/creator_register.html', user_role=user_role)


    
    
def get_user_role(user_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT role
        FROM users
        WHERE id = ?;
    ''', (user_id,))
    role = cursor.fetchone()
    conn.close()
    return role[0] if role else None







@creator_dashboard_bp.route('/register_as_creator', methods=['POST'])
def register_as_creator():
    user_id = session.get('user_id')

    if user_id:
        user_role = get_user_role(user_id)

        if user_role == 'user':
            upgrade_to_creator(user_id)
            return redirect(url_for('creator_dashboard.display_creator_dashboard'))

    

def upgrade_to_creator(user_id):

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('''
            update users
            set role = 'creator'
            where id = ?;
        ''', (user_id,))

        conn.commit()
        conn.close()
        
        
@creator_dashboard_bp.route('/edit_song/<int:song_id>', methods=['GET', 'POST'])
def edit_song(song_id):
    user_id = session.get('user_id')
    user_role = get_user_role(user_id)
    if session.get('blacklisted') == 1:
        
        return "You are blacklisted as a creator because you have violated our policies. If you yhink it is a mistake lease contact app admin on mad1@app"

    if user_role == 'creator':
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        if request.method == 'GET':
           
            cursor.execute("select id, title, artist, genre, rating from songs WHERE id = ? AND creator_id = ?;", (song_id, user_id))
            song = cursor.fetchone()

            if song:
                return render_template('creator/creator_edit_song.html', song=song, song_id=song_id)
            else:
                return "Song not found or you don't have permission to edit it."

        elif request.method == 'POST':
            
            cursor.execute("SELECT id, title, artist, genre, rating, lyrics FROM songs WHERE id = ? AND creator_id = ?;", (song_id, user_id))
            existing_song = cursor.fetchone()

            
            title = request.form.get('title', existing_song[1])
            artist = request.form.get('artist', existing_song[2])
            genre = request.form.get('genre', existing_song[3])
            rating = request.form.get('rating', existing_song[4])
            lyrics = request.form.get('lyrics', existing_song[5])


            cursor.execute("UPDATE songs SET title = ?, artist = ?, genre = ?, rating = ?,  lyrics = ? WHERE id = ? AND creator_id = ?;",
                           (title, artist, genre, rating, lyrics, song_id, user_id))
            conn.commit()

            conn.close()

            return redirect(url_for('creator_dashboard.display_creator_dashboard'))

    return "Unauthorized access."



@creator_dashboard_bp.route('/delete_song/<int:song_id>', methods=['POST'])
def delete_song(song_id):
    user_id = session.get('user_id')
    user_role = get_user_role(user_id)

    if user_role == 'creator':
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        
        cursor.execute("SELECT id FROM songs WHERE id = ? AND creator_id = ?;", (song_id, user_id))
        existing_song = cursor.fetchone()

        if existing_song:
            
            cursor.execute("delete from  songs WHERE id = ? AND creator_id = ?;", (song_id, user_id))
            conn.commit()
            conn.close()

            return redirect(url_for('creator_dashboard.display_creator_dashboard'))

    return "Unauthorized access or song not found."





UPLOAD_FOLDER = 'app/uploads'
ALLOWED_EXTENSIONS = {'mp3'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@creator_dashboard_bp.route('/upload_song', methods=['GET', 'POST'])
def display_upload_form():
    user_id = session.get('user_id')
    user_role = get_user_role(user_id)
    
    if session.get('blacklisted') == 1:
        return "You are blacklisted as a creator because you have violated our policies. If you think it is a mistake, please contact app admin on mad1@app"

    if user_role == 'creator':
        # Fetch existing albums for the creator
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, artist_name FROM albums WHERE creator_id = ?;", (user_id,))
        albums = cursor.fetchall()
        conn.close()

        if request.method == 'GET':
            # Display the song upload form with the list of existing albums
            return render_template('creator/creator_upload_song.html', albums=albums)

        elif request.method == 'POST':
            # Process the form submission to create a new song
            title = request.form.get('title')
            artist = request.form.get('artist')
            genre = request.form.get('genre')
            lyrics = request.form.get('lyrics')
            album_id = request.form.get('album')  # Album selected in the form

            # Handle the optional audio file upload
            audio_data = None
            if 'audio_file' in request.files:
                audio_file = request.files['audio_file']
                if audio_file.filename != '' and allowed_file(audio_file.filename):
                    audio_data = audio_file.read()  # Read the binary data of the audio file

            # Save the new song to the database
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO songs (title, artist, genre, album_id, creator_id, rating, num_ratings, lyrics, audio) VALUES (?, ?, ?, ?, ?, 0, 0, ?, ?);",
                           (title, artist, genre, album_id, user_id, lyrics, audio_data))
            conn.commit()
            conn.close()

            return redirect(url_for('creator_dashboard.display_creator_dashboard'))

    return "Unauthorized access"
        
        
        
        
@creator_dashboard_bp.route('/play_audio/<int:song_id>', methods=['GET'])
def play_audio(song_id):
    # Retrieve the audio data for the specified song_id from the database
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT audio FROM songs WHERE id = ?;", (song_id,))
    audio_data = cursor.fetchone()
    conn.close()

    if audio_data:
        # Serve the audio data
        return send_file(io.BytesIO(audio_data[0]), mimetype='audio/mp3')
@creator_dashboard_bp.route('/creator_edit_album', methods=['GET'])
def display_creator_edit_album():
    
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM albums;")
    all_albums = cursor.fetchall()
    conn.close()

    return render_template('creator/creator_edit_album.html', all_albums=all_albums)


@creator_dashboard_bp.route('/edit_album/<int:album_id>', methods=['GET', 'POST'])
def edit_album(album_id):
    if request.method == 'POST':
        
        name = request.form.get('name')
        genre = request.form.get('genre')
        artist_name = request.form.get('artist_name')

        
        conn = sqlite3.connect('database.db')  
        cursor = conn.cursor()
        cursor.execute("UPDATE albums SET name=?, genre=?, artist_name=? WHERE id=?;",
                       (name, genre, artist_name, album_id))
        conn.commit()
        conn.close()

        flash('Album updated successfully', 'success')
        return redirect(url_for('creator_dashboard.display_creator_edit_album'))
    else:
        
        conn = sqlite3.connect('database.db')  
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM albums WHERE id = ?;", (album_id,))
        album = cursor.fetchone()
        conn.close()

        if album:
            return render_template('creator/creator_edit_album.html', album=album)
        else:
            flash('Album not found', 'error')
            return redirect(url_for('creator_dashboard.display_creator_edit_album'))




@creator_dashboard_bp.route('/delete_album/<int:album_id>', methods=['GET'])
def delete_album(album_id):
    
    conn = sqlite3.connect('database.db')  
    cursor = conn.cursor()

    
    cursor.execute("SELECT id FROM songs WHERE album_id = ?;", (album_id,))
    song_ids = cursor.fetchall()

    
    cursor.execute("DELETE FROM albums WHERE id = ?;", (album_id,))
    cursor.execute("DELETE FROM songs WHERE album_id = ?;", (album_id,))

    
    conn.commit()
    conn.close()

    
    

    return redirect(url_for('creator_dashboard.display_creator_edit_album'))



@creator_dashboard_bp.route('/add_album', methods=['POST'])
def add_album():
    if request.method == 'POST':
        creator_id = session.get('user_id')  
        name = request.form.get('new_name')
        genre = None
        artist_name = request.form.get('new_artist_name')

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("insert into albums (name, genre, artist_name, creator_id) VALUES (?, ?, ?, ?);",
                       (name, genre, artist_name, creator_id))
        conn.commit()
        conn.close()

        
        return redirect(url_for('creator_dashboard.display_creator_edit_album'))

    
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("select* FROM albums;")
    all_albums = cursor.fetchall()
    conn.close()

    return render_template('creator/creator_edit_album.html', all_albums=all_albums)