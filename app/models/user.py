from app.extensions import db

class User(db.Model):
    __tablename__ = 'User'
    user_id = db.Column(db.String(45), primary_key=True)
    password = db.Column(db.String(16), nullable=False) 
    country = db.Column(db.String(5), default=None)  
    spotifyid = db.Column(db.String(45), default=None)  
    last_sid = db.Column(db.String(45), default=None) 
    
    def __repr__(self):
        return '<User %r>' % self.user_id

class Friendship(db.Model):
    __tablename__ = 'Friendship'
    user1_id = db.Column(db.String(45), db.ForeignKey('User.user_id'), primary_key=True)  
    user2_id = db.Column(db.String(45), db.ForeignKey('User.user_id'), primary_key=True) 
    status = db.Column(db.Enum('pending', 'accepted', 'rejected', 'cancelled'), default='pending')
    
    user1 = db.relationship('User', foreign_keys=[user1_id], back_populates='friendships1') 
    user2 = db.relationship('User', foreign_keys=[user2_id], back_populates='friendships2')  

    def __repr__(self):
        return '<Friendship %r - %r>' % (self.user1_id, self.user2_id)
