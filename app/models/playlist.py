from app.extensions import db

class Playlist(db.Model):
    __tablename__ = 'Playlist'
    playlist_id = db.Column(db.String(45), primary_key=True)
    user_id = db.Column(db.String(45), db.ForeignKey('User.user_id'))
    playlist_name = db.Column(db.String(45), default=None)
    rate = db.Column(db.Float, default=None)
    
    user = db.relationship('User', back_populates='playlists')

    def __repr__(self):
        return '<Playlist %r>' % self.playlist_id

class SongPlaylist(db.Model):
    __tablename__ = 'SongPlaylist'
    song_id = db.Column(db.String(45), db.ForeignKey('Song.song_id'), primary_key=True)  # FOREIGN KEY ve PRIMARY KEY
    playlist_id = db.Column(db.String(45), db.ForeignKey('Playlist.playlist_id'), primary_key=True)  # FOREIGN KEY ve PRIMARY KEY
    
    song = db.relationship('Song', back_populates='playlists')  # İlişkiyi tanımlayın
    playlist = db.relationship('Playlist', back_populates='songs')  # İlişkiyi tanımlayın

    def __repr__(self):
        return '<SongPlaylist %r - %r>' % (self.song_id, self.playlist_id)
