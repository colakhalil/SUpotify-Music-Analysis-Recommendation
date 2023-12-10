from flask import Blueprint, Flask, request, url_for, session, jsonify, redirect
from flask_cors import CORS, cross_origin
from spotipy.oauth2 import SpotifyOAuth 
import spotipy
import requests
import time 
import json  
from . import db
from .models import Album, Friendship, RateSong, SongPlaylist, Playlist, Artist, Song, User


auth = Blueprint('auth', __name__) 


TOKEN_INFO = "token_info" 

client_id = "26136d6b22c945479934e5eac513a86b"
client_secret = "24c7dc28107c4c1a8f72920e2c9b5845"
# scope tanimi 
def create_spotify_outh():
    return SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=url_for("auth.redirect_page", _external=True),  # Make sure this matches the registered redirect URI
        #scope="user-read-playback-state user-read-private user-read-email user-follow-read user-top-read",
        scope="user-read-recently-played playlist-read-private user-read-playback-state user-read-private user-read-email user-follow-read user-top-read",
    ) 
    
def create_spotify_outh_mobile():
    return SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=url_for("auth.redirect_mobile", _external=True),  # Make sure this matches the registered redirect URI
        #scope="user-read-playback-state user-read-private user-read-email user-follow-read user-top-read",
        scope="user-read-recently-played playlist-read-private user-read-playback-state user-read-private user-read-email user-follow-read user-top-read",
    ) 

@auth.route('/sign_up', methods=['POST', 'GET'])
def sign_up():
    if request.method == "POST":
        data = request.get_json()

        existing_user = User.query.filter_by(user_id=data['user_id']).first()
        if existing_user:
            return jsonify({'message': False})

        new_user = User(user_id=data['user_id'], password=data['password'], email=data['email'])
        db.session.add(new_user)
        db.session.commit()
        
        added_user = User.query.filter_by(user_id=data['user_id']).first()
        
        if added_user:
            return jsonify({"message": True})
        else:
            return jsonify({"message": False})

        

@auth.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        
        data = request.get_json()
        email = data['email']
        entered_password = data['password']
        
        user = User.query.filter_by(email=email).first()
    
        if user:
            password_from_db = user.password
            if password_from_db == entered_password:
                return jsonify({"message": True})
            else:
                return jsonify({"message": False})
        else:
            return jsonify({"message": False})

# spotify login 
@auth.route('/sauth')
def login_spotify():
    auth_url = create_spotify_outh().get_authorize_url()
    return redirect(auth_url)

@auth.route('/sauth_mobile')
def login_spotify_mobile():
    auth_url = create_spotify_outh_mobile().get_authorize_url()
    return redirect(auth_url)

@auth.route("/redirect")
def redirect_page():
    
    session.clear()
    code = request.args.get("code")
    token_info = create_spotify_outh().get_access_token(code)
    session[TOKEN_INFO] = token_info
    
    spotify = spotipy.Spotify(auth=token_info['access_token'])
    user_data = spotify.current_user()
    
    user = User.query.filter_by(email=user_data["email"]).first()

    if user:
        user.spotify_id = user_data["id"]
        user.country = user_data["country"]
        user.profile_pic = user_data["images"][0]["url"]

        db.session.commit()
    
    return redirect("http://127.0.0.1:8008/token_add")

@auth.route("/redirect_mobile")
def redirect_mobile():
    
    session.clear()
    code = request.args.get("code")
    token_info = create_spotify_outh().get_access_token(code)
    session[TOKEN_INFO] = token_info
    
    spotify = spotipy.Spotify(auth=token_info['access_token'])
    user_data = spotify.current_user()
    
    user = User.query.filter_by(email=user_data["email"]).first()

    if user:
        user.spotify_id = user_data["id"]
        user.country = user_data["country"]
        user.profile_pic = user_data["images"][0]["url"]

        db.session.commit()
    
    return redirect("http://127.0.0.1:8008/token_add_mobile")