from app.extensions import db

class Artist(db.Model):
    __tablename__ = 'Artist'
    artist_id = db.Column(db.String(45), primary_key=True)
    popularity = db.Column(db.Integer, nullable=False)
    artist_name = db.Column(db.String(45), nullable=False)
    genres = db.Column(db.JSON, nullable=False)
    follower = db.Column(db.Integer, nullable=False)
    rate = db.Column(db.Float, nullable=False)
    
    def __repr__(self):
        return '<Artist %r>' % self.artist_id
