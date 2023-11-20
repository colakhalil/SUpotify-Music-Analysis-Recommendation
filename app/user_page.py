from flask import Blueprint, Flask, request, url_for, session, jsonify, redirect
from flask_cors import CORS, cross_origin
from spotipy.oauth2 import SpotifyOAuth 
from sqlalchemy import or_
from sqlalchemy.orm import aliased
import spotipy
import requests
import time 
import json
from . import db 
from .models import Album, Friendship, RateSong, SongPlaylist, Playlist, Artist, Song, User

user = Blueprint('user', __name__)

TOKEN_INFO = "token_info" 

client_id = "e3bb122dc61347a6b496d5f15a036a68"
client_secret = "e217a887698a43479bcbcc3698853677"

@user.route('/user_data/<email>', methods=['GET'])
def user_page(email):
    
    user = User.query.filter_by(email=email).first()
    if user:
        user_info = {
            'user_id': user.user_id,
            'profile_pic': user.profile_pic,
            'last_sid': user.last_sid
        }
    else:
        return jsonify({'message': False})
    
    UserAlias = aliased(User)

    friends_query = (
        db.session.query(User.user_id)
        .join(Friendship, or_(Friendship.user1_id == User.user_id, Friendship.user2_id == User.user_id))
        .filter(or_(Friendship.user1_id == user_info['user_id'], Friendship.user2_id == user_info['user_id']))
    )

    friends = friends_query.all()
    
    return jsonify({
        'user_id': user.user_id,
        'profile_pic': user.profile_pic,
        'last_sid': user.last_sid,
        'friends': friends,
        'friend_count': len(friends)
    })
