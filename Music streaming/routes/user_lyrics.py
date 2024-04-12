from flask import Blueprint, render_template,request,redirect,url_for,session,abort
import sqlite3

from routes.user_home import user_home_bp ,get_songs
user_lyrics_bp = Blueprint('user_lyrics', __name__, url_prefix='/user_lyrics')



@user_lyrics_bp.route('/<int:song_id>')
def get_lyrics(song_id):
    
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("select * from songs where id = ?;", (song_id,))
    song = cursor.fetchone()
    cursor.execute("select * from albums where id = ?",(song[1],))
    album_name = cursor.fetchall()
    
    if song:
        
        cursor.execute("update songs set clicks = clicks + 1 WHERE id = ?;", (song_id,))


        
        cursor.execute("select * from songs where id = ?;", (song_id,))

        updated_song = cursor.fetchone()
        conn.commit()
        conn.close()

        song_lyrics = updated_song[4]
        song_artist = updated_song[6]
        song_title = updated_song[2]
        song_rating = round(float(updated_song[7]), 1)

        return render_template('user_home/lyrics.html', song_lyrics=song_lyrics, song_title=song_title, song_artist=song_artist, song_id=song_id, song_rating=song_rating,album_name=album_name)
    else:
        abort(404, description="Song not found")
        
        
        
        
        
@user_lyrics_bp.route('/rate/<int:song_id>', methods=['POST'])
def rate_song(song_id):
    rating = request.form.get('rating')

    if rating is not None:
        rating = float(rating)

        
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE songs SET rating = (rating * num_ratings + ?) / (num_ratings + 1), num_ratings = num_ratings + 1 WHERE id = ?", (rating, song_id))
        conn.commit()
        conn.close()

    
    return redirect(url_for('user_lyrics.get_lyrics', song_id=song_id))