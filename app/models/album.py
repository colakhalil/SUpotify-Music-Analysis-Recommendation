from app.extensions import db

class Album(db.Model):
    __tablename__ = 'Album'
    album_id = db.Column(db.String(45), primary_key=True)
    artist_id = db.Column(db.String(45), db.ForeignKey('Artist.artist_id'))  # FOREIGN KEY
    rate = db.Column(db.Float, default=None)
    type = db.Column(db.String(15), default=None)
    
    artist = db.relationship('Artist', back_populates='albums')  # İlişkiyi tanımlayın

    def __repr__(self):
        return '<Album %r>' % self.album_id
