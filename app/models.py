from . import db
from flask_login import UserMixin
from datetime import datetime


class Album(db.Model):
    __tablename__ = 'Album'

    album_id = db.Column(db.String(45), primary_key=True)
    artist_id = db.Column(db.String(45), db.ForeignKey('Artist.artist_id'))
    rate = db.Column(db.Float)
    album_type = db.Column(db.String(15))
    image = db.Column(db.String(200))

    #artist = db.relationship('Artist', back_populates='albums', foreign_keys=[artist_id])

class Artist(db.Model):
    __tablename__ = 'Artist'

    artist_id = db.Column(db.String(45), primary_key=True)
    popularity = db.Column(db.Integer)
    artist_name = db.Column(db.String(45))
    genres = db.Column(db.JSON)
    follower = db.Column(db.Integer)
    rate = db.Column(db.Float)
    
    #albums = db.relationship('Album', back_populates='artist', foreign_keys=[artist_id])

class Friendship(db.Model):
    __tablename__ = 'Friendship'

    # Both user_ids have arg primary_key=True because their combination forms the Primary Key
    user1_id = db.Column(db.String(45), db.ForeignKey('User.user_id'), primary_key=True)
    user2_id = db.Column(db.String(45), db.ForeignKey('User.user_id'), primary_key=True)

    user1 = db.relationship('User', foreign_keys=[user1_id])
    user2 = db.relationship('User', foreign_keys=[user2_id])


class RateSong(db.Model):
    __tablename__ = 'RateSong'

    song_id = db.Column(db.String(45), db.ForeignKey('Song.song_id'), primary_key=True)
    user_id = db.Column(db.String(45), db.ForeignKey('User.user_id'), primary_key=True)
    rating = db.Column(db.Integer)

    # Define the relationships with the Song and User tables
    song = db.relationship('Song', foreign_keys=[song_id])
    user = db.relationship('User', foreign_keys=[user_id])


class SongPlaylist(db.Model):
    __tablename__ = 'SongPlaylist'

    # Both song_id and playlist_id have arg primary_key=True because their combination forms the Primary Key
    song_id = db.Column(db.String(45), db.ForeignKey('Song.song_id'), primary_key=True)
    playlist_id = db.Column(db.String(45), db.ForeignKey('Playlist.playlist_id'), primary_key=True)

    # Define the relationships with the Song and Playlist tables
    song = db.relationship('Song', foreign_keys=[song_id])
    playlist = db.relationship('Playlist', foreign_keys=[playlist_id])

class Playlist(db.Model):
    __tablename__ = 'Playlist'

    playlist_id = db.Column(db.String(45), primary_key=True)
    user_id = db.Column(db.String(45), db.ForeignKey('User.user_id'))
    playlist_name = db.Column(db.String(45))
    rate = db.Column(db.Float)
    picture = db.Column(db.String(200))


class Song(db.Model):
    __tablename__ = 'Song'

    song_id = db.Column(db.String(45), primary_key=True)
    artist_id = db.Column(db.String(45), db.ForeignKey('Artist.artist_id'))
    album_id = db.Column(db.String(45), db.ForeignKey('Album.album_id'))
    song_name = db.Column(db.String(100))
    picture = db.Column(db.Text)
    rate = db.Column(db.Float)
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

    #artist = db.relationship('Artist', back_populates='songs', foreign_keys=[artist_id])
    #album = db.relationship('Album', back_populates='songs', foreign_keys=[album_id])


class User(db.Model):
    __tablename__ = 'User'

    user_id = db.Column(db.String(45), primary_key=True)
    password = db.Column(db.String(16), nullable=False)
    country = db.Column(db.String(5))
    spotify_id = db.Column(db.String(45))
    #last_sid = db.Column(db.String(45), db.ForeignKey('Song.song_id'))
    email = db.Column(db.String(150), nullable=False)
    profile_pic = db.Column(db.String(200))

    # Define the relationship with the Song table
    #last_song = db.relationship('Song', foreign_keys=[last_sid])


