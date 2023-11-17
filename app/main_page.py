from flask import Blueprint, Flask, request, url_for, session, jsonify, redirect
from flask_mysqldb import MySQL
from flask_cors import CORS, cross_origin
from spotipy.oauth2 import SpotifyOAuth 
import spotipy
import requests
import time 
import json  
from . import db 

main = Blueprint('main', __name__)

TOKEN_INFO = "token_info" 

client_id = "e3bb122dc61347a6b496d5f15a036a68"
client_secret = "e217a887698a43479bcbcc3698853677"

def fetch_and_store_song_info(sp, song_id):
    # Spotify API'yi kullanarak şarkı bilgilerini al
    track_info = sp.track(song_id)
    
    # Albüm bilgilerini al
    album_info = sp.album(track_info['album']['id'])
    
    
    # Sanatçı bilgilerini al
    artist_info = sp.artist(track_info['artists'][0]['id'])
    
    # Veritabanına bilgileri eklemek için gerekli alanları seç
    data = {
        'song_id': track_info['id'],
        'artist_id': track_info['artists'][0]['id'],
        'album_id': track_info['album']['id'],
        'rate': None,  # Buraya isteğe bağlı bir değer ekleyebilirsiniz
        'tempo': None,  # Buraya isteğe bağlı bir değer ekleyebilirsiniz
        'popularity': track_info['popularity'],
        'valence': None,  # Buraya isteğe bağlı bir değer ekleyebilirsiniz  
        'duration': track_info['duration_ms'],
        'energy': None,  # Buraya isteğe bağlı bir değer ekleyebilirsiniz 
        'danceability': None,  # Buraya isteğe bağlı bir değer ekleyebilirsiniz 
    }
    
    # Veritabanına ekleme işlemi
    #cur = mysql.connection.cursor()
    #cur.execute("""
    #    INSERT INTO `Song` (
    #        `song_id`, `artist_id`, `album_id`, `rate`, `tempo`, `popularity`, `valence`, `duration`, `energy`, `danceability`
    #    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    #""", (
    #    data['song_id'], data['artist_id'], data['album_id'], data['rate'], data['tempo'],
    #    data['popularity'], data['valence'], data['duration'], data['energy'], data['danceability']
    #))
    #mysql.connection.commit()
    #cur.close()

@main.route('/recommendations/<genre>')
def get_recommendations_by_genre(genre):

    sp = spotipy.Spotify(auth=session[TOKEN_INFO]['access_token'])
    recommendations = sp.recommendations(seed_genres=[genre], limit=10)

    for track in recommendations['tracks']:
        fetch_and_store_song_info(sp, track['id'])

    song_list = [
        {
            'song_id': track['id'],
            'artist_id': track['artists'][0]['id'],
            'album_id': track['album']['id'],
            'rate': None,  # Buraya isteğe bağlı bir değer ekleyebilirsiniz
            'tempo': None,  # Buraya isteğe bağlı bir değer ekleyebilirsiniz
            'popularity': track['popularity'],
            'valence': None,  # Buraya isteğe bağlı bir değer ekleyebilirsiniz
            'duration': track['duration_ms'],
            'energy': None,  # Buraya isteğe bağlı bir değer ekleyebilirsiniz
            'danceability': None,  # Buraya isteğe bağlı bir değer ekleyebilirsiniz
            'name': track['name'],
            'artists': ', '.join(artist['name'] for artist in track['artists']),
            'album': {
                'name': track['album']['name'],
                'release_date': track['album']['release_date'],
                'image': track['album']['images'][0]['url']
            }
        }
        for track in recommendations['tracks']
    ] 
    # JSON formatında şarkı ve albüm bilgilerini döndür
    return jsonify(song_list) 
## not : cekebilecegi ornek genres Pop rock , hiphop , electronic county , jazz , blues , rnb , reggae , classical 

@main.route('/get_song_info/<song_id>') 
def fetch_and_store_song_info(song_id):
    
        sp = spotipy.Spotify(auth=session['token_info']['access_token'])
        # Spotify API'yi kullanarak şarkı bilgilerini al
        track_info = sp.track(song_id)
        
        # Albüm bilgilerini al
        album_info = sp.album(track_info['album']['id'])
        
        
        # Sanatçı bilgilerini al
        artist_info = sp.artist(track_info['artists'][0]['id'])
        
        # Veritabanına bilgileri eklemek için gerekli alanları seç
        data = {
            'song_id': track_info['id'],
            'artist_id': track_info['artists'][0]['id'],
            'album_id': track_info['album']['id'],
            'rate': None,  # Buraya isteğe bağlı bir değer ekleyebilirsiniz
            'tempo': None,  # Buraya isteğe bağlı bir değer ekleyebilirsiniz
            'popularity': track_info['popularity'],
            'valence': None,  # Buraya isteğe bağlı bir değer ekleyebilirsiniz  
            'duration': track_info['duration_ms'],
            'energy': None,  # Buraya isteğe bağlı bir değer ekleyebilirsiniz 
            'danceability': None,  # Buraya isteğe bağlı bir değer ekleyebilirsiniz 
        }
        
        # Veritabanına ekleme işlemi
        #cur = mysql.connection.cursor()
        #cur.execute("""
        #    INSERT INTO `Song` (
        #        `song_id`, `artist_id`, `album_id`, `rate`, `tempo`, `popularity`, `valence`, `duration`, `energy`, `danceability`
        #    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        #""", (
        #    data['song_id'], data['artist_id'], data['album_id'], data['rate'], data['tempo'],
        #    data['popularity'], data['valence'], data['duration'], data['energy'], data['danceability']
        #))
        #mysql.connection.commit()
        #cur.close()
        
        return jsonify(data)   
    
@main.route('/get_user_playlists')
def get_user_playlists():
    # Kullanıcının çalma listelerini al
    sp = spotipy.Spotify(auth=session['token_info']['access_token'])
    user_playlists = sp.current_user_playlists()

    # Kullanıcının çalma listelerini belirtilen formata dönüştür
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
