from flask import Blueprint, Flask, request, url_for, session, jsonify, redirect
from flask_cors import CORS, cross_origin
from spotipy.oauth2 import SpotifyOAuth 
import lyricsgenius as lg
import spotipy
import requests
import time 
import json
from datetime import datetime
from . import db 
from .models import Album, Friendship, RateSong, SongPlaylist, Playlist, Artist, Song, User

main = Blueprint('main', __name__)

TOKEN_INFO = "token_info" 

client_id = "e3bb122dc61347a6b496d5f15a036a68"
client_secret = "e217a887698a43479bcbcc3698853677"

GENIUS_API_KEY = "ELYRzAgCM0wR2jm42T8YVN3sJZMXH4Yss-hBIERYV4xFp2RJGiRbrfnuQh5gqJfg"

@main.route("/lyrics/<artist_name>/<song_name>")
def lyrics(artist_name, song_name):
    
    #DB check must be done here
    
    genius = lg.Genius(GENIUS_API_KEY)
    song = genius.search_song(title = song_name, artist = artist_name)
    
    return jsonify(song.lyrics)

def fetch_and_store_song_info(sp, song_id):

    track_info = sp.track(song_id)
    
    audio_features = sp.audio_features(song_id)[0]
    
    data = {
        'song_id': track_info['id'],
        'artist_id': track_info['artists'][0]['id'],
        'album_id': track_info['album']['id'],
        'song_name': track_info['name'],
        'picture': track_info['album']['images'][0]['url'],
        'rate': 0,
        'play_count': 0,
        'tempo': audio_features['tempo'],  
        'popularity': track_info['popularity'],
        'valence': audio_features['valence'],  
        'duration': track_info['duration_ms'],
        'energy': audio_features['energy'],  
        'danceability': audio_features['danceability'],
        'genre': track_info['atists'][0]['genres'],
        'release_date': track_info['album']['release_date'],
        'date_added': datetime.now().strftime("%Y-%m-%d")
    }
    # dict unpacking
    new_song = Song(**data)

    db.session.add(new_song)
    db.session.commit()
    
@main.route('/save_song/<songid>', methods=['GET, POST'])
def save_song(songid):
    if request.method == 'POST':
        sp = spotipy.Spotify(auth=session['token_info']['access_token'])
        fetch_and_store_song_info(sp, songid)
        
        return jsonify({'message': True})


@main.route('/recommendations/<genre>')
def get_recommendations_by_genre(genre):

    sp = spotipy.Spotify(auth=session[TOKEN_INFO]['access_token'])
    recommendations = sp.recommendations(seed_genres=[genre], limit=10)

    return jsonify(recommendations)

@main.route('/song_info/<user_id>/<song_id>') 
def get_song_info(song_id, user_id):
    song = Song.query.filter_by(song_id=song_id).first()
    
    if song:
        
        prev_rate = RateSong.query.filter_by(song_id=song_id, user_id=user_id).first()
        
        song_info = {
            'song_id': song.song_id,
            'artists': song.artist_id.artist_name,
            'title': song.song_name,
            'thumbnail': song.picture,
            'rateAvg': song.rate,
            'playCount': song.play_count,
            'popularity': song.popularity,
            'valence': song.valence,
            'duration': song.duration,
            'genre': song.genre,
            'releaseYear': song.release_date,
            'dateAdded': song.date_added,
            'userPrevRating': prev_rate.rating if prev_rate else 0
        }
        return jsonify(song_info)
    else:
        return jsonify({"message": False})


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

    # if playlist exists, update it; else create new
    for playlist_data in formatted_playlists:
        existing_playlist = Playlist.query.filter_by(playlist_id=playlist_data['playlistID']).first()

        if existing_playlist:
            existing_playlist.playlist_name = playlist_data['name']
            existing_playlist.picture = playlist_data["playlistPic"]
            existing_playlist.song_number = playlist_data['songNumber']
        else:
            new_playlist = Playlist(
                playlist_id=playlist_data['playlistID'],
                playlist_name=playlist_data['name'],
                picture=playlist_data["playlistPic"],
                song_number=playlist_data['songNumber']
            )
            db.session.add(new_playlist)
    db.session.commit()
    return jsonify(formatted_playlists) 

@main.route('/change_rating', methods=['GET', 'POST'])
def change_rating():
    if request.method == 'POST':
        data = request.get_json()
        prev_rate = RateSong.query.filter_by(song_id=data['song_id'], user_id=data['user_id']).first()
        
        if prev_rate:
            RateSong.query.filter_by(song_id=data['song_id'], user_id=data['user_id']).update({'rating': data['rating']})
        else:
            new_rate = RateSong(
                song_id=data['song_id'],
                user_id=data['user_id'],
                rating=data['rating']
            )
            db.session.add(new_rate)
        
        db.session.commit()
        
        return jsonify({'message': True})
    
    
@main.route('/song_played', methods=['GET', 'POST'])
def song_played():
    if request.method == 'POST':
        data = request.get_json()
        song = Song.query.filter_by(song_id=data['song_id']).first()
        user = User.query.filter_by(user_id=data['user_id']).first()
        if song:
            song.play_count += 1
            user.last_sid = song.song_id
            db.session.commit()
            return jsonify({'message': True})
        else:
            return jsonify({'message': False})
        
        
@main.route('/search/<query>', methods=['GET'])
def search(query):
    sp = spotipy.Spotify(auth=session['token_info']['access_token'])
    search_result = sp.search(q=query, type = "track", limit=10)
    
    formatted_result = [
        {
            'song_id': song['id'],
            'artist': song['artists'][0]['name'],
            'title': song['name'],
            'thumbnail': song['album']['images'][0]['url'],
            'popularity': song['popularity']
        }
        for song in search_result['tracks']['items']
    ]
    
    return jsonify(formatted_result)

@main.route("/get_playlist_info/<playlist_id>")
def get_playlist_info(playlist_id):
    sp = spotipy.Spotify(auth=session['token_info']['access_token'])
    playlist_info = sp.playlist(playlist_id)
    song_list = []
 
    for i in range(len(playlist_info['tracks']['items'])):  

        s = RateSong.query.filter_by(song_id=playlist_info['tracks']['items'][i]['track']['id']).all()
        
        song_1 = {
            'song_id' : playlist_info['tracks']['items'][i]['track']['id'],
            'song_name' : playlist_info['tracks']['items'][i]['track']['name'],
            'duration' : playlist_info['tracks']['items'][i]['track']['duration_ms'],
            'release_year' : playlist_info['tracks']['items'][i]['track']['album']['release_date'],
            'artist' : playlist_info['tracks']['items'][i]['track']['artists'][0]['name'],
            'song_rating' : s.rate if s else 0
        }

        song_list.append(song_1) 
    data = {
        'playlisID': playlist_id,
        'playlistName': playlist_info['name'],
        'playlistPicture': playlist_info['images'][0]['url'],
        'songs' : song_list
        }
    
    return jsonify(data)