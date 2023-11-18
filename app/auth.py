from flask import Blueprint, Flask, request, url_for, session, jsonify, redirect
from flask_mysqldb import MySQL
from flask_cors import CORS, cross_origin
from spotipy.oauth2 import SpotifyOAuth 
import spotipy
import requests
import time 
import json  
from . import db 


auth = Blueprint('auth', __name__) 

user_table_query = """
CREATE TABLE IF NOT EXISTS `User` (
  `user_id` varchar(45) NOT NULL,
  `password` varchar(16) NOT NULL,
  `country` varchar(5) DEFAULT NULL,
  `spotifyid` varchar(45) DEFAULT NULL,
  `last_sid` varchar(45) DEFAULT NULL,
  `email` varchar(150) NOT NULL,
  'profile_pic' varchar(200) DEFAULT NULL,
  PRIMARY KEY (`user_id`)
)"""

insert_user_query = """
INSERT INTO `User` (`user_id`, `password`, `email`)
VALUES (%s, %s, %s)
"""
select_user_query = "SELECT * FROM User" 


TOKEN_INFO = "token_info" 

client_id = "e3bb122dc61347a6b496d5f15a036a68"
client_secret = "e217a887698a43479bcbcc3698853677"

# scope tanimi 
def create_spotify_outh():
    return SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=url_for("auth.redirect_page", _external=True),  # Make sure this matches the registered redirect URI
        #scope="user-read-playback-state user-read-private user-read-email user-follow-read user-top-read",
        scope="user-read-recently-played playlist-read-private user-read-playback-state user-read-private user-read-email user-follow-read user-top-read",
    ) 

@auth.route('/sign_up', methods=['POST', 'GET'])
def sign_up():
    if request.method == "POST":
        data = request.get_json()
        
        cur = db.connection.cursor()
        
        # Create the User table if it doesn't exist
        cur.execute(user_table_query)
        
        query = """SELECT * FROM User WHERE user_id = %s"""
        cur.execute(query, (data["user_id"],))
        db_data = cur.fetchone()
        
        if db_data:
            return jsonify({"message": False})
        
        # Insert user data into the User table
        cur.execute(insert_user_query, (data["user_id"], data["password"], data["email"]))
        db.connection.commit()
        
        cur.close()
        return jsonify({"message": True})
        

@auth.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")
        
        cur = db.connection.cursor()
        query = """SELECT password FROM User WHERE email = %s"""
        cur.execute(query, (email,))
        user_data = cur.fetchone()
        cur.close()
        if user_data:
            if user_data["password"] == password:
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
 
@auth.route("/redirect")
def redirect_page():
    session.clear()
    code = request.args.get("code")
    token_info = create_spotify_outh().get_access_token(code)
    session[TOKEN_INFO] = token_info
    
    spotify = spotipy.Spotify(auth=token_info['access_token'])
    user_data = spotify.current_user()
    
    cur = db.connection.cursor()
    
    update_query = """
        UPDATE `User`
        SET `spotifyid` = %s, `country` = %s, 'profile_pic' = %s
        WHERE `email` = %s
    """
    cur.execute(update_query, (user_data["id"], user_data["country"], user_data["email"], user_data["images"][0]["url"]))
    return redirect("http://localhost:3000/main") 