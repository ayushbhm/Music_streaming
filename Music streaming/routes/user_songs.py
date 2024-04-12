from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import sqlite3
from routes.user_home import get_songs

user_songs_bp = Blueprint('user_songs', __name__, url_prefix='/user_songs')

@user_songs_bp.route('/all_songs')
def display_all_songs():
    all_songs = get_songs()
    return render_template('user_home/all_songs.html',all_songs=all_songs)