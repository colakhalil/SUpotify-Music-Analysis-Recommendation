from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
from flask_migrate import Migrate
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth 
from datetime import datetime
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
    
    CORS(app, supports_credentials=True)

    from .auth import auth
    from .main_page import main
    from .user_page import user
    
    
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(main, url_prefix='/')
    app.register_blueprint(user, url_prefix='/')
    
    from .models import Album, Friendship, RateSong, SongPlaylist, Playlist, Artist, Song, User
    
    with app.app_context():
        db.create_all()
        # This part is for adding mock data to db
        # To run the app properly, make sure to comment out below

        if not User.query.first():
            new_user = User(user_id='atakan', password='PW', email='atakan.demirel@sabanciuniv.edu')
            new_user2 = User(user_id='umit', password='PW', email='umit.colak@sabanciuniv.edu')
            new_user3 = User(user_id='bercin', password='PW', email='bercin.idk@sabanciuniv.edu')
            new_user4 = User(user_id='furkan', password='PW', email='femre@sabanciuniv.edu')
            new_user5 = User(user_id='ayca', password='PW', email='ayca@sabanciuniv.edu')
            new_user6 = User(user_id='idil', password='PW', email='idil@sabanciuniv.edu')
            new_user7 = User(user_id='halil', password='PW', email='halil@sabanciuniv.edu')
            new_user8 = User(user_id='arda', password='PW', email='arda@sabanciuniv.edu')
            new_user9 = User(user_id='ezgi', password='PW', email='ezgi@sabanciuniv.edu')
            
            db.session.add(new_user)
            db.session.add(new_user2)
            db.session.add(new_user3)
            db.session.add(new_user4)
            db.session.add(new_user5)
            db.session.add(new_user6)
            db.session.add(new_user7)
            db.session.add(new_user8)
            db.session.add(new_user9)
            
            db.session.commit()

            friendship1 = Friendship(user1_id='atakan', user2_id='bercin')
            friendship2 = Friendship(user1_id='atakan', user2_id='umit')
            friendship3 = Friendship(user1_id='umit', user2_id='bercin')
            friendship4 = Friendship(user1_id='umit', user2_id='furkan')
            friendship5 = Friendship(user1_id='umit', user2_id='ayca')
            friendship6 = Friendship(user1_id='umit', user2_id='idil')
            friendship7 = Friendship(user1_id='umit', user2_id='halil')
            friendship8 = Friendship(user1_id='umit', user2_id='arda')
            friendship9 = Friendship(user1_id='umit', user2_id='ezgi')
            friendship10 = Friendship(user1_id='bercin', user2_id='furkan')
            friendship11 = Friendship(user1_id='bercin', user2_id='ayca')
            friendship12 = Friendship(user1_id='bercin', user2_id='idil')
            friendship13 = Friendship(user1_id='bercin', user2_id='halil')
            friendship14 = Friendship(user1_id='bercin', user2_id='arda')
            friendship15 = Friendship(user1_id='bercin', user2_id='ezgi')
            friendship16 = Friendship(user1_id='furkan', user2_id='ayca')
            friendship17 = Friendship(user1_id='furkan', user2_id='idil')
            friendship18 = Friendship(user1_id='furkan', user2_id='halil')
            

            db.session.add(friendship1)
            db.session.add(friendship2)
            db.session.add(friendship3)
            db.session.add(friendship4)
            db.session.add(friendship5)
            db.session.add(friendship6)
            db.session.add(friendship7)
            db.session.add(friendship8)
            db.session.add(friendship9)
            db.session.add(friendship10)
            db.session.add(friendship11)
            db.session.add(friendship12)
            db.session.add(friendship13)
            db.session.add(friendship14)
            db.session.add(friendship15)
            db.session.add(friendship16)
            db.session.add(friendship17)
            db.session.add(friendship18)
            db.session.commit()
        
        
    
    return app
