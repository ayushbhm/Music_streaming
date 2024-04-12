from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import sqlite3


admin_manage_bp = Blueprint('admin_manage', __name__, url_prefix='/admin_manage')


@admin_manage_bp.route('/')
def admin_manage():
   
    creators = get_creators()
    songs = get_songs()

    return render_template('admin/admin_manage.html', creators=creators, songs=songs)

def get_creators():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE role='creator';")
    creators = cursor.fetchall()
    conn.close()
    return creators


def get_songs():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("select * from songs;")
    songs = cursor.fetchall()
    conn.close()
    return songs


@admin_manage_bp.route('/blacklist_creator/<int:user_id>')
def blacklist_creator(user_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("update users set blacklisted = 1 WHERE id = ?;", (user_id,))
    conn.commit()
    conn.close()

    return redirect(url_for('admin_manage.admin_manage'))




@admin_manage_bp.route('/unblacklist_creator/<int:user_id>')
def unblacklist_creator(user_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("update users set blacklisted = 0 WHERE id = ?;", (user_id,))
    conn.commit()
    conn.close()

    return redirect(url_for('admin_manage.admin_manage'))





@admin_manage_bp.route('/delete_song/<int:song_id>')
def delete_song(song_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # You might need to add additional logic to delete the song from your database
    cursor.execute("DELETE FROM songs WHERE id = ?;", (song_id,))
    
    conn.commit()
    conn.close()
    
    flash("Song deleted successfully.", "success")
    
    return redirect(url_for('admin_manage.admin_manage'))
