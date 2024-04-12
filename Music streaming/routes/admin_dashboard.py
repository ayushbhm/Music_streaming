from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import sqlite3

admin_dashboard_bp = Blueprint('admin_dashboard', __name__, url_prefix='/admin_dashboard')

@admin_dashboard_bp.route('/')
def admin_dashboard():
    try:
        user_count = get_statistic_count("users", "role='user'")
        creator_count = get_statistic_count("users", "role='creator'")
        song_count = get_statistic_count("songs")
        album_count = get_statistic_count("albums")
        playlist_count = get_statistic_count("playlist")

        top_songs = get_top_songs(3)
        top_genres = get_top_genres(3)

        return render_template('admin/admin_dashboard.html', user_count=user_count, creator_count=creator_count,
                               song_count=song_count, album_count=album_count, playlist_count=playlist_count,
                               top_songs=top_songs, top_genres=top_genres)
    except Exception as e:
        return render_template('admin_dashboard.html')

def get_statistic_count(table_name, condition=None):
    con = sqlite3.connect('database.db')
    cursor = con.cursor()

    try:
        if condition:
            query = f"select count(*) from {table_name} where {condition};"
        else:
            query = f"select count(*) from {table_name};"

        cursor.execute(query)
        count = cursor.fetchone()[0]

        print(f"Count for {table_name}: {count}")
        return count
    finally:
        con.close()

def get_top_songs(n):
    con = sqlite3.connect('database.db')
    cursor = con.cursor()

    cursor.execute("select * from songs order by clicks desc limit ?;", (n,))
    top_songs = cursor.fetchall()

    con.close()
    return top_songs

def get_top_genres(n):
    con = sqlite3.connect('database.db')
    cursor = con.cursor()

    cursor.execute("select genre, sum(clicks) as total_clicks from songs group by genre order by total_clicks desc limit ?;", (n,))
    top_genres = cursor.fetchall()

    con.close()
    return top_genres
