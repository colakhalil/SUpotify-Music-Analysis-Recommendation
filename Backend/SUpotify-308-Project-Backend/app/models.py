from . import db
from flask_login import UserMixin
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.String(45), primary_key=True)
    password = db.Column(db.String(16), nullable=False)
    country = db.Column(db.String(5))
    spotify_id = db.Column(db.String(45))
    last_sid = db.Column(db.String(45), db.ForeignKey('songs.song_id'))
    email = db.Column(db.String(150), nullable=False)
    profile_pic = db.Column(db.String(200))
    #token = db.Column(db.String(200))
    last_song = db.relationship('Song', foreign_keys=[last_sid])
    playlists = db.relationship('Playlist', back_populates='user', lazy='dynamic')
    #friendships = db.relationship('Friendship', back_populates='user1', lazy='dynamic')
    friendships = db.relationship('Friendship', foreign_keys='Friendship.user1_id', backref='user')
    friendships = db.relationship('Friendship', foreign_keys='Friendship.user2_id', backref='user')
    rated_songs = db.relationship('RateSong', back_populates='user', lazy='dynamic')
    rated_albums = db.relationship('RateAlbum', back_populates='user', lazy='dynamic')
    rated_artists = db.relationship('RateArtist', back_populates='user', lazy='dynamic')

class Friendship(db.Model):
    __tablename__ = 'friendships'

    user1_id = db.Column(db.String(45), db.ForeignKey('users.user_id'), primary_key=True)
    user2_id = db.Column(db.String(45), db.ForeignKey('users.user_id'), primary_key=True)
    rate_sharing = db.Column(db.String(10), default='private')
    
    user1 = db.relationship('User', foreign_keys=[user1_id], back_populates='friendships')
    user2 = db.relationship('User', foreign_keys=[user2_id])

class RateSong(db.Model):
    __tablename__ = 'rate_songs'

    song_id = db.Column(db.String(45), db.ForeignKey('songs.song_id'), primary_key=True)
    user_id = db.Column(db.String(45), db.ForeignKey('users.user_id'), primary_key=True)
    rating = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, default=datetime.now)

    song = db.relationship('Song', foreign_keys=[song_id])
    user = db.relationship('User', foreign_keys=[user_id], back_populates='rated_songs')

class SongPlaylist(db.Model):
    __tablename__ = 'song_playlists'

    song_id = db.Column(db.String(45), db.ForeignKey('songs.song_id'), primary_key=True)
    playlist_id = db.Column(db.String(45), db.ForeignKey('playlists.playlist_id'), primary_key=True)

    song = db.relationship('Song', foreign_keys=[song_id])
    playlist = db.relationship('Playlist', foreign_keys=[playlist_id])

class Playlist(db.Model):
    __tablename__ = 'playlists'

    playlist_id = db.Column(db.String(45), primary_key=True)
    user_id = db.Column(db.String(45), db.ForeignKey('users.user_id'))
    playlist_name = db.Column(db.String(45))
    rate = db.Column(db.Float)
    picture = db.Column(db.String(200))
    song_number = db.Column(db.Integer)

    user = db.relationship('User', foreign_keys=[user_id], back_populates='playlists')

class Song(db.Model):
    __tablename__ = 'songs'

    song_id = db.Column(db.String(45), primary_key=True)
    artist_id = db.Column(db.String(45), db.ForeignKey('artists.artist_id'))
    album_id = db.Column(db.String(45), db.ForeignKey('albums.album_id'))
    song_name = db.Column(db.String(100))
    picture = db.Column(db.Text)
    tempo = db.Column(db.Integer)
    popularity = db.Column(db.Integer)
    valence = db.Column(db.Float)
    duration = db.Column(db.Integer)
    energy = db.Column(db.Float)
    danceability = db.Column(db.Float)
    genre = db.Column(db.Text)
    release_date = db.Column(db.Integer)
    play_count = db.Column(db.Integer)
    lyrics = db.Column(db.Text)
    date_added = db.Column(db.DateTime, default=datetime.now)

    artist = db.relationship('Artist', foreign_keys=[artist_id], back_populates='songs')
    album = db.relationship('Album', foreign_keys=[album_id], back_populates='songs')

class Album(db.Model):
    __tablename__ = 'albums'

    album_id = db.Column(db.String(45), primary_key=True)
    album_name = db.Column(db.String(100))
    artist_id = db.Column(db.String(45), db.ForeignKey('artists.artist_id'))
    album_type = db.Column(db.String(15))
    image = db.Column(db.String(200))

    artist = db.relationship('Artist', foreign_keys=[artist_id], back_populates='albums')
    songs = db.relationship('Song', back_populates='album', lazy='dynamic')

class Artist(db.Model):
    __tablename__ = 'artists'

    artist_id = db.Column(db.String(45), primary_key=True)
    popularity = db.Column(db.Integer)
    artist_name = db.Column(db.String(45))
    genres = db.Column(db.String(100))
    followers = db.Column(db.Integer)
    picture = db.Column(db.String(200))

    albums = db.relationship('Album', back_populates='artist', lazy='dynamic')
    songs = db.relationship('Song', back_populates='artist', lazy='dynamic')

class RateAlbum(db.Model):
    _tablename_ = 'rate_albums'

    album_id = db.Column(db.String(45), db.ForeignKey('albums.album_id'), primary_key=True)
    user_id = db.Column(db.String(45), db.ForeignKey('users.user_id'), primary_key=True)
    rating = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, default=datetime.now)
    album = db.relationship('Album', foreign_keys=[album_id])
    user = db.relationship('User', foreign_keys=[user_id], back_populates='rated_albums')

class RateArtist(db.Model):
    _tablename_ = 'rate_artists'

    artist_id = db.Column(db.String(45), db.ForeignKey('artists.artist_id'), primary_key=True)
    user_id = db.Column(db.String(45), db.ForeignKey('users.user_id'), primary_key=True)
    rating = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, default=datetime.now)
    artist = db.relationship('Artist', foreign_keys=[artist_id])
    user = db.relationship('User', foreign_keys=[user_id], back_populates='rated_artists')
    
class ArtistsOfSong(db.Model):
    tablename = 'song_artists'

    song_id = db.Column(db.String(45), db.ForeignKey('songs.song_id'), primary_key=True)
    artist_id = db.Column(db.String(45), db.ForeignKey('artists.artist_id'), primary_key=True)