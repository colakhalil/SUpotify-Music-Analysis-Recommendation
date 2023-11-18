from flask import Blueprint, Flask, request, url_for, session, jsonify, redirect
from flask_mysqldb import MySQL
from flask_cors import CORS, cross_origin
from spotipy.oauth2 import SpotifyOAuth 
import spotipy
import requests
import time 
import json
from datetime import datetime
from . import db 

main = Blueprint('main', __name__)

TOKEN_INFO = "token_info" 

client_id = "e3bb122dc61347a6b496d5f15a036a68"
client_secret = "e217a887698a43479bcbcc3698853677"

def fetch_and_store_song_info(sp, song_id):

    track_info = sp.track(song_id)
    
    audio_features = sp.audio_features(song_id)[0]
    
    data = {
        'song_id': track_info['id'],
        'artist_id': track_info['artists'][0]['id'],
        'album_id': track_info['album']['id'],
        'rate': 0,
        'play_count': 0,
        'tempo': audio_features['tempo'],  
        'popularity': track_info['popularity'],
        'valence': audio_features['valence'],  
        'duration': track_info['duration_ms'],
        'energy': audio_features['energy'],  
        'danceability': audio_features['danceability'],
        'song_name': track_info['name'],
        'picture': track_info['album']['images'][0]['url'],
        'genre': track_info['atists'][0]['genres'],
        'release_date': track_info['album']['release_date'],
        'date_added': datetime.now().strftime("%Y-%m-%d")
    }
    
    cur = db.connection.cursor()
    cur.execute("""
        INSERT INTO `Song` (`song_id`, `artist_id`, `album_id`, `rate`, `play_count`, `tempo`, `popularity`, `valence`, `duration`, `energy`, `danceability`, `song_name`, `picture`, `genre`, `release_date`, `date_added`)
        VALUES (%(song_id)s, %(artist_id)s, %(album_id)s, %(rate)s, %(play_count)s, %(tempo)s, %(popularity)s, %(valence)s, %(duration)s, %(energy)s, %(danceability)s, %(song_name)s, %(picture)s, %(genre)s, %(release_date)s, %(date_added)s)
    """, data)
    db.connection.commit()
    cur.close()

@main.route('/recommendations/<genre>')
def get_recommendations_by_genre(genre):

    sp = spotipy.Spotify(auth=session[TOKEN_INFO]['access_token'])
    recommendations = sp.recommendations(seed_genres=[genre], limit=10)

    return jsonify(recommendations)
## not : cekebilecegi ornek genres Pop rock , hiphop , electronic county , jazz , blues , rnb , reggae , classical 

@main.route('/get_song_info/<song_id>') 
def get_song_info(song_id):
    
    cur = db.connection.cursor()
    cur.execute("""
        SELECT * FROM `Song` WHERE `song_id` = %s
    """, (song_id,))
    
    song_info = cur.fetchone()
    cur.close()
    return jsonify(song_info)   

@main.route('/get_user_playlists')
def get_user_playlists():
    
    sp = spotipy.Spotify(auth=session['token_info']['access_token'])
    user_playlists = sp.current_user_playlists()

    formatted_playlists = [
        {
            "name": playlist['name'],
            "playlistPic": playlist['images'][0]['url'] if playlist['images'] else None,
            "songNumber": playlist['tracks']['total'],
            "playlistID": playlist['id']
        }
        for playlist in user_playlists['items']
    ]
    return jsonify(formatted_playlists) 