from flask import Flask,render_template
app = Flask(__name__)
from routes.auth import auth_bp; app.register_blueprint(auth_bp)
from routes.search import search_bp; app.register_blueprint(search_bp)

from routes.user_lyrics import user_lyrics_bp;app.register_blueprint(user_lyrics_bp)

from routes.user_home import user_home_bp;app.register_blueprint(user_home_bp,url_prefix='/user')
from routes.user_playlists import user_playlists_bp;app.register_blueprint(user_playlists_bp)

from routes.user_create_playlist import user_create_playlists_bp;app.register_blueprint(user_create_playlists_bp)

from routes.user_songs import user_songs_bp;app.register_blueprint(user_songs_bp)
from routes.creator_dashboard import creator_dashboard_bp;app.register_blueprint(creator_dashboard_bp)
from routes.admin_dashboard import admin_dashboard_bp;app.register_blueprint(admin_dashboard_bp)

from routes.admin_manage import admin_manage_bp;app.register_blueprint(admin_manage_bp)

UPLOAD_FOLDER = 'app/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
'''from routes.admin_routes import admin_bp
''''REgistering all blueprints that we want to use'''
'''

app.register_blueprint(admin_bp)


UPLOAD_FOLDER = 'static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
'''


@app.route('/')
def index():
    return render_template('home.html')





app.secret_key = 'secret_key_for_grocery-_tore'

app.debug = True
if __name__ == '__main__': 
 app.run(port=5001)


