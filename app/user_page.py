from flask import Blueprint, Flask, request, url_for, session, jsonify, redirect
from flask_cors import CORS, cross_origin
from spotipy.oauth2 import SpotifyOAuth 
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
            'profile_pic': user.image,
            'last_sid': user.last_sid
        }
    else:
        return jsonify("There are no users with given email")
    
    friends = User.query.join(
            Friendship,
            ((Friendship.user1_id == User.user_id) | (Friendship.user2_id == User.user_id))
        ).filter(
            (Friendship.user1_id == user.user_id) | (Friendship.user2_id == user.user_id)
        ).with_entities(
            User.user_id,
            User.profile_pic,
            User.last_sid
        ).all()
    
    return jsonify({
        'user_id': user.user_id,
        'profile_pic': user.profile_pic,
        'last_sid': user.last_sid
    } for user in friends)