from flask import Blueprint, Flask, request, url_for, session, jsonify, redirect
from flask_cors import CORS, cross_origin
from spotipy.oauth2 import SpotifyOAuth 
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
    
    sp = spotipy.Spotify(auth=session['token_info']['access_token'])
    fetch_and_store_song_info(sp, songid)
    
    return jsonify({'message': 'Song saved successfully'})


@main.route('/recommendations/<genre>')
def get_recommendations_by_genre(genre):

    sp = spotipy.Spotify(auth=session[TOKEN_INFO]['access_token'])
    recommendations = sp.recommendations(seed_genres=[genre], limit=10)

    return jsonify(recommendations)

@main.route('/get_song_info/<song_id>') 
def get_song_info(song_id):
    
    song = Song.query.filter_by(song_id=song_id).first()
    if song:
        song_info = {
            'song_id': song.song_id,
            'artist_id': song.artist_id,
            'album_id': song.album_id,
            'song_name': song.song_name,
            'picture': song.picture,
            'rate': song.rate,
            'play_count': song.play_count,
            'tempo': song.tempo,
            'popularity': song.popularity,
            'valence': song.valence,
            'duration': song.duration,
            'energy': song.energy,
            'danceability': song.danceability,
            'genre': song.genre,
            'release_date': song.release_date,
            'date_added': song.date_added
        }
        return jsonify(song_info)
    else:
        return jsonify({"message": "Song not found"})

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

    return jsonify(formatted_playlists) 
