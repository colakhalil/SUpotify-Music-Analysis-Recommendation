from app.extensions import db

class Song(db.Model):
    __tablename__ = 'Song'
    song_id = db.Column(db.String(45), primary_key=True)
    artist_id = db.Column(db.String(45), db.ForeignKey('Artist.artist_id')) 
    album_id = db.Column(db.String(45), db.ForeignKey('Album.album_id')) 
    name = db.Column(db.String(45), default=None)
    rate = db.Column(db.Float, default=None)  
    tempo = db.Column(db.Integer, default=None)
    popularity = db.Column(db.Integer, default=None)
    valence = db.Column(db.Float, default=None)
    duration = db.Column(db.Integer, default=None)
    energy = db.Column(db.Float, default=None)
    danceability = db.Column(db.Float, default=None)
    
    artist = db.relationship('Artist', back_populates='songs') 
    album = db.relationship('Album', back_populates='songs')

    def __repr__(self):
        return '<Song %r>' % self.song_id
