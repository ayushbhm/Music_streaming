from flask import Blueprint, url_for,render_template,session ,request,redirect
import sqlite3

search_bp = Blueprint('search', __name__, url_prefix='/search')



@search_bp.route('/search', methods=['GET'])
def search_results():
    search_query = request.args.get('search_query', '')
    print("Search Query:", search_query) 

    
    song_results = []
    songs_of_album = []

    
    if search_query:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        
        cursor.execute("SELECT * FROM songs WHERE title LIKE ? OR artist LIKE ? OR genre LIKE ?;", ('%' + search_query + '%', '%' + search_query + '%', '%' + search_query + '%'))
        song_results = cursor.fetchall()

        
        cursor.execute("SELECT * FROM albums WHERE name LIKE ?;", ('%' + search_query + '%',))
        album_results = cursor.fetchall()

        
        for album in album_results:
            cursor.execute("SELECT * FROM songs WHERE album_id = ?;", (album[0],))
            songs_of_album.extend(cursor.fetchall())
            
        user_id = session.get('user_id')
        cursor.execute("SELECT * FROM playlist WHERE name LIKE ? AND user_id = ?;", ('%' + search_query + '%', user_id))
        playlist_results = cursor.fetchall()

        conn.close()
    else:
        
        song_results = []

    return render_template('search.html', song_results=song_results, songs_of_album=songs_of_album,playlist_results=playlist_results)


@search_bp.route('/admin_search', methods=['GET'])
def admin_search_results():
    search_query = request.args.get('search_query', '')
    print("Search Query:", search_query) 

    
    song_results = []
    songs_of_album = []

    
    if search_query:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        
        cursor.execute("select * from songs WHERE title LIKE ? OR artist LIKE ? OR genre LIKE ?;", ('%' + search_query + '%', '%' + search_query + '%', '%' + search_query + '%'))
        song_results = cursor.fetchall()

        
        cursor.execute("SELECT * FROM albums WHERE name LIKE ?;", ('%' + search_query + '%',))
        album_results = cursor.fetchall()

        
        for album in album_results:
            cursor.execute("SELECT * FROM songs WHERE album_id = ?;", (album[0],))
            songs_of_album.extend(cursor.fetchall())
            

        conn.close()
    else:
        
        song_results = []

    return render_template('admin_search.html', song_results=song_results, songs_of_album=songs_of_album)

            
        
        
