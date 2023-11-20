from flask import Blueprint, Flask, request, url_for, session, jsonify, redirect
from flask_mysqldb import MySQL
from flask_cors import CORS, cross_origin
from spotipy.oauth2 import SpotifyOAuth 
import spotipy
import requests
import time 
import json  
from . import db 

user = Blueprint('user', __name__)

TOKEN_INFO = "token_info" 

client_id = "e3bb122dc61347a6b496d5f15a036a68"
client_secret = "e217a887698a43479bcbcc3698853677"

create_friendship_table = """
CREATE TABLE IF NOT EXISTS `Friendship` (
  `user1_id` varchar(45) NOT NULL,
  `user2_id` varchar(45) NOT NULL,
  PRIMARY KEY (`user1_id`,`user2_id`),
  KEY `user2_id` (`user2_id`),
  CONSTRAINT `friendship_ibfk_1` FOREIGN KEY (`user1_id`) REFERENCES `User` (`user_id`),
  CONSTRAINT `friendship_ibfk_2` FOREIGN KEY (`user2_id`) REFERENCES `User` (`user_id`)
)
"""

@user.route('/user_data/<email>', methods=['GET'])
def user_page(email):
    
    sp = spotipy.Spotify(auth=session[TOKEN_INFO]['access_token'])
    
    profile_pic = sp.current_user()['images'][0]['url']
    
    cur = db.connection.cursor()
    
    cur.execute("""
        SELECT user_id, last_sid FROM `User` WHERE `email` = %s
    """, (email,))
    user = cur.fetchone()
    
    cur.execute("""
        SELECT User.user_id
        FROM Friendship
        JOIN User ON (Friendship.user1_id = User.user_id OR Friendship.user2_id = User.user_id)
        WHERE (Friendship.user1_id = %s OR Friendship.user2_id = %s)
        """, (user['user_id'], user['user_id']))
    friends = cur.fetchall()
    
    cur.close()
    return jsonify({
        'username': user['user_id'],
        'profile_pic': profile_pic,
        'last_sid': user['last_sid'],
        'friends': friends,
        'friend_count': len(friends)
    })
