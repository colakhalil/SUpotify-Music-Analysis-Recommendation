from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
from flask_migrate import Migrate
from os import path
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth 
import spotipy
from datetime import datetime

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

        # This part is for adding mock data to db
        # To run the app properly, make sure to comment out below

        client_id_Atakan = "e67f3a00be3044b89f2d3629f497b344"
        client_secret_Atakan = "2eaa1a9033d6460f84cdbb0fd17479d5"

        client_credentials_manager = SpotifyClientCredentials(client_id=client_id_Atakan, client_secret=client_secret_Atakan)
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


        new_user = User(user_id='ATAKAN', password='PW', email='atakan.demirel@sabanciuniv.edu')
        new_user2 = User(user_id='EREN', password='PW', email='eren.akgun@sabanciuniv.edu')
        new_user3 = User(user_id='BERÇİN', password='PW', email='bercin.idk@sabanciuniv.edu')

        db.session.add(new_user)
        db.session.add(new_user2)
        db.session.add(new_user3)
        db.session.commit()

        friendship1 = Friendship(user1_id='ATAKAN', user2_id='EREN')
        friendship2 = Friendship(user1_id='EREN', user2_id='BERÇİN')

        db.session.add(friendship1)
        db.session.add(friendship2)
        db.session.commit()

        added_user = User.query.filter_by(user_id='ATAKAN').first()
        if added_user:
            print('ALL FINE')
        else:
            print('NOT SO FINE')

        # Search for the playlist by name
        playlist_name = 'Top 100 Artists (Monthly Listenership)'
        results = sp.search(q=playlist_name, type='playlist')
        playlist = results['playlists']['items'][0]
        playlist_id = playlist['id']

        playlist_info = {
            "playlist_name": playlist['name'],
            "picture": playlist['images'][0]['url'] if playlist['images'] else None,
            "song_number": playlist['tracks']['total'],
            "playlist_id": playlist['id'],
            "user_id": "ATAKAN"
        }
        
        tracks = sp.playlist_tracks(playlist_id, limit=10)
        for item in tracks['items']:
            track_info = item['track']
            song_id = track_info['id']
            audio_features = sp.audio_features(song_id)[0]
            new_song = Song(
                song_id = track_info['id'],
                artist_id = track_info['artists'][0]['id'],
                album_id = track_info['album']['id'],
                song_name = track_info['name'],
                picture = track_info['album']['images'][0]['url'],
                rate = 0,
                play_count = 0,
                tempo = audio_features['tempo'],  
                popularity = track_info['popularity'],
                valence = audio_features['valence'],  
                duration = track_info['duration_ms'],
                energy = audio_features['energy'],  
                danceability = audio_features['danceability'],
                genre= track_info['artists'][0].get('genres', 'Unknown Genre'),
                release_date = track_info['album']['release_date'],
                date_added = datetime.now()
            )

            song_rating = RateSong(song_id=track_info['id'], user_id='ATAKAN', rating = 3)
            db.session.add(new_song)
            db.session.add(song_rating)
            db.session.commit()

        # dict unpacking
        new_playlist = Playlist(**playlist_info)

        db.session.add(new_playlist)
        db.session.commit()

        users = User.query.all()
        songs = Song.query.all()
        friendships = Friendship.query.all()

        for user in users:
            print(user.user_id)

        for song in songs:
            print(song.song_name)

        for fs in friendships:
            print('New Friendship')
            print(fs.user1_id)
            print(fs.user2_id)
            print(fs.user1.user_id)
            print(fs.user2.user_id)

        # Mock Ends Here
    
    return app
