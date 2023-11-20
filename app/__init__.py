from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
from flask_migrate import Migrate
from os import path

db = SQLAlchemy()
#migrate = Migrate()
DB_NAME = "supotify_database"

def create_app(): 
    app = Flask(__name__)
    app.config["SESSION_COOKIE_NAME"] = "spotify_cookie"
    app.config['SECRET_KEY'] = 'hjs'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    
    db.init_app(app)
    #migrate.init_app(app, db)
    
    CORS(app, resources={
        r"/sign_up": {"origins": "http://localhost:3000"},
        r"/login": {"origins": "http://localhost:3000"},
        r"/sauth": {"origins": "http://localhost:3000"}
    })

    from .auth import auth
    from .main_page import main
    from .user_page import user
    
    
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(main, url_prefix='/')
    app.register_blueprint(user, url_prefix='/')
    
    from .models import Album, Friendship, RateSong, SongPlaylist, Playlist, Artist, Song, User
    
    with app.app_context():
        db.drop_all()
        db.create_all()
    
    return app
