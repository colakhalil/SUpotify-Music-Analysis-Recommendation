from app.extensions import db

class RateAlbum(db.Model):
    __tablename__ = 'RateAlbum'
    user_id = db.Column(db.String(45), db.ForeignKey('User.user_id'), primary_key=True)  # FOREIGN KEY ve PRIMARY KEY
    album_id = db.Column(db.String(45), db.ForeignKey('Album.album_id'), primary_key=True)  # FOREIGN KEY ve PRIMARY KEY
    rate = db.Column(db.Float, default=None)
    
    user = db.relationship('User', back_populates='rated_albums')  # İlişkiyi tanımlayın
    album = db.relationship('Album', back_populates='ratings')  # İlişkiyi tanımlayın

    def __repr__(self):
        return '<RateAlbum %r - %r>' % (self.user_id, self.album_id)

class RateArtist(db.Model):
    __tablename__ = 'RateArtist'
    user_id = db.Column(db.String(45), db.ForeignKey('User.user_id'), primary_key=True)  # FOREIGN KEY ve PRIMARY KEY
    artist_id = db.Column(db.String(45), db.ForeignKey('Artist.artist_id'), primary_key=True)  # FOREIGN KEY ve PRIMARY KEY
    rate = db.Column(db.Float, default=None)
    
    user = db.relationship('User', back_populates='rated_artists')  # İlişkiyi tanımlayın
    artist = db.relationship('Artist', back_populates='ratings')  # İlişkiyi tanımlayın

    def __repr__(self):
        return '<RateArtist %r - %r>' % (self.user_id, self.artist_id)
    
class RatePlaylist(db.Model):
    __tablename__ = 'RatePlaylist'
    user_id = db.Column(db.String(45), db.ForeignKey('User.user_id'), primary_key=True)  # FOREIGN KEY ve PRIMARY KEY
    playlist_id = db.Column(db.String(45), db.ForeignKey('Playlist.playlist_id'), primary_key=True)  # FOREIGN KEY ve PRIMARY KEY
    rate = db.Column(db.Float, default=None)
    
    user = db.relationship('User', back_populates='rated_playlists')  # İlişkiyi tanımlayın
    playlist = db.relationship('Playlist', back_populates='ratings')  # İlişkiyi tanımlayın

    def __repr__(self):
        return '<RatePlaylist %r - %r>' % (self.user_id, self.playlist_id)
    
class RateSong(db.Model):
    __tablename__ = 'RateSong'
    song_id = db.Column(db.String(45), db.ForeignKey('Song.song_id'), primary_key=True)  # FOREIGN KEY ve PRIMARY KEY
    user_id = db.Column(db.String(45), db.ForeignKey('User.user_id'), primary_key=True)  # FOREIGN KEY ve PRIMARY KEY
    rate = db.Column(db.Float, default=None)
    
    song = db.relationship('Song', back_populates='ratings')  # İlişkiyi tanımlayın
    user = db.relationship('User', back_populates='rated_songs')  # İlişkiyi tanımlayın

    def __repr__(self):
        return '<RateSong %r - %r>' % (self.song_id, self.user_id)