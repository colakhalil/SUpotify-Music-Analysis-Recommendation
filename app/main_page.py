from flask import Blueprint, Flask, render_template, request, url_for, session, jsonify, redirect
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
    
    new_song = Song(
                song_id = track_info['id'],
                artist_id = track_info['artists'][0]['id'],
                album_id = track_info['album']['id'],
                song_name = track_info['name'],
                picture = track_info['album']['images'][0]['url'],
                rate = 0,
                play_count = 0,
                tempo = audio_features['tempo'],  
                popularity = track_info['popularity'],
                valence = audio_features['valence'],  
                duration = track_info['duration_ms'],
                energy = audio_features['energy'],  
                danceability = audio_features['danceability'],
                genre= ', '.join(track_info['atists'][0]['genres']),
                release_date = track_info['album']['release_date'],
                date_added = datetime.now()
            )

    db.session.add(new_song)
    db.session.commit()
    
@main.route('/save_song/<songid>', methods=['GET, POST'])
def save_song(songid):
    if request.method == 'POST':
        sp = spotipy.Spotify(auth=session['token_info']['access_token'])
        fetch_and_store_song_info(sp, songid)
        
        return jsonify({'message': True})

from threading import Thread
import time
from flask import jsonify
# updated spotify function !!!!! 
@main.route('/recommendations/<genre>')
@cross_origin()
def get_recommendations_by_genre(genre):
    def fetch_spotify_recommendations():
        nonlocal recommendations, success
        try:
            sp = spotipy.Spotify(auth=token)
            recommendations = sp.recommendations(seed_genres=[genre], limit=10)
            success = True
        except:
            success = False

    recommendations = None
    success = False
    spotify_thread = Thread(target=fetch_spotify_recommendations)
    spotify_thread.start()
    spotify_thread.join(timeout=5)

    if success and recommendations:
        result = []
        for track in recommendations['tracks']:
            curr_track = {
                'song_id': track['id'],
                'song_name': track['name'],
                'artist_name': [artist['name'] for artist in track['artists']],
                'picture': track['album']['images'][0]['url'],
                'songLength': track['duration_ms'],
            }
            result.append(curr_track)
        return jsonify(result)
    else:
        # Fetch songs from the database
        songs = Song.query.filter_by(genre=genre).all()
        db_result = []
        for song in songs:
            db_song = {
                'song_id': song.song_id,
                'song_name': song.song_name,
                'artist_name': song.artist.artist_name if song.artist else '',
                'picture': song.picture,
                'songLength': song.duration,
            }
            db_result.append(db_song)
        return jsonify(db_result)
   

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

        playlist_tracks = sp.playlist_tracks(playlist_data['playlistID'])
    for track in playlist_tracks['items']:
        track_info = track['track']

        # Veritabanında aynı song_id'ye sahip bir kayıt var mı kontrol et
        existing_track = Song.query.filter_by(song_id=track_info['id']).first()

        if existing_track:
            # Eğer varsa, var olan kaydı güncelle
            existing_track.song_name = track_info['name']
            existing_track.picture = track_info['album']['images'][0]['url']
            existing_track.popularity = track_info['popularity']
            existing_track.release_date = track_info['album']['release_date']
            existing_track.date_added = datetime.now()
        else:
            # Eğer yoksa, yeni kaydı ekle

            
            new_track = Song(
                song_id=track_info['id'],
                artist_id=track_info['artists'][0]['id'],
                album_id=track_info['album']['id'],
                song_name=track_info['name'],
                picture=track_info['album']['images'][0]['url'],
                rate=0,
                play_count=0,
                tempo=0,
                popularity=track_info['popularity'],
                valence=0,
                duration=0,
                energy=0,
                danceability=0,
                ##genre=', '.join(track_info['artists'][0]['genres']),
                release_date=track_info['album']['release_date'],
                date_added=datetime.now()
            )
            db.session.add(new_track) 

    db.session.commit()
    return jsonify(formatted_playlists) 


@main.route('/show_database')
def show_database():
    playlists = Playlist.query.all()
    tracks = Song.query.all()

 
    print("\nSong:")
    for track in tracks:
        print(f"ID: {track.song_id}, Name: {track.song_name}, Rate: {track.rate}, Play Count: {track.play_count}, Tempo: {track.tempo}, Popularity: {track.popularity}, Valence: {track.valence}, Duration: {track.duration}, Energy: {track.energy}, Danceability: {track.danceability}, Genre: {track.genre}, Release Date: {track.release_date}, Date Added: {track.date_added}")
    
    return jsonify({'message': True})
    # Eğer bir web sayfasında görmek istiyorsanız, render_template kullanabilirsiniz
    #return render_template('show_database.html', playlists=playlists, tracks=tracks)
 
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


@main.route('/<user_id>/90s', methods=['GET'])
def get_user_most_liked_90s_songs(user_id):
    try:
        # Query to get the most liked songs from the 90s for a specific user
        most_liked_songs_90s = (
            db.session.query(Song)
            .join(RateSong, (Song.song_id == RateSong.song_id))
            .join(User, (User.user_id == RateSong.user_id))
            .filter(
                User.user_id == user_id,
                (Song.release_date >= 1990) & (Song.release_date <= 1999),
            )
            .order_by(RateSong.rating.desc())  # Assuming 'rating' is the column indicating user ratings
            .limit(5)
            .all()
        )

        # Format the response
        result = {
            'user_id': user_id,
            'most_liked_songs_90s': [
                {
                    'title': song.song_name,
                    'artist': song.artist.artist_name,
                    'releaseYear': song.release_date,
                }
                for song in most_liked_songs_90s
                for user_rating in song.rated_songs
                if user_rating.user_id == user_id
            ],
        }

        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)}) 


from sqlalchemy import func    

@main.route('/allSongs', methods=['GET'])
def get_all_songs():
    try:
        # Query all songs from the database
        all_songs = Song.query.all()

        # Format the response as an array of JSON objects
        songs_json = [
            {
                'song_id': song.song_id,
                'artist_name': song.artist.artist_name,
                'album_name': song.album.album_name,
                'song_name': song.song_name,
                'picture': song.picture,
                'rate': song.rate,
                'tempo': song.tempo,
                'popularity': song.popularity,
                'valence': song.valence,
                'duration': song.duration,
                'energy': song.energy,
                'danceability': song.danceability,
                'genre': song.genre,
                'release_date': song.release_date,
                'play_count': song.play_count,
                'lyrics': song.lyrics,
                'date_added': song.date_added.isoformat() if song.date_added else None,
            }
            for song in all_songs
        ]

        return jsonify({'songs': songs_json})

    except Exception as e:
        return jsonify({'error': str(e)})        
    

from sqlalchemy import or_
@main.route('/search_item/<search_term>', methods=['GET'])
def search_item(search_term):
    try:
        # Search for songs, albums, artists, and friends in the database based on the search term
        song_results = Song.query.filter(or_(Song.song_name.ilike(f"%{search_term}%"), Song.artist_id.ilike(f"%{search_term}%"))).all()
        album_results = Album.query.filter(or_(Album.album_name.ilike(f"%{search_term}%"), Album.artist_id.ilike(f"%{search_term}%"))).all()
        artist_results = Artist.query.filter(Artist.artist_name.ilike(f"%{search_term}%")).all()
         
        # Format the response
        result = {
            'songs': [
                {
                    'song_id': song.song_id,
                    'song_name': song.song_name,
                    'artist_id': song.artist_id,
                    'release_date': song.release_date,
                }
                for song in song_results
            ],
            'albums': [
                {
                    'album_id': album.album_id,
                    'album_name': album.album_name,
                    'artist_id': album.artist_id,
        
                }
                for album in album_results
            ],
            'artists': [
                {
                    'artist_id': artist.artist_id,
                    'artist_name': artist.artist_name,
                    'popularity': artist.popularity,
                }
                for artist in artist_results
            ],
     
        }

        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)}) 
    
@main.route('/searchFriends/<user_id>/<search_term>', methods=['GET'])
def search_friends(user_id, search_term):
    try:
        # Find the user by user_id
        user = User.query.get(user_id)

        if not user:
            return jsonify({'error': 'User not found.'})

        # Search for friends of the user based on the search term
        friends_results = (
            Friendship.query
            .filter(
                ((Friendship.user1_id == user_id) & Friendship.user2_id.ilike(f"%{search_term}%"))
                | ((Friendship.user2_id == user_id) & Friendship.user1_id.ilike(f"%{search_term}%"))
            )
            .all()
        )

        # Format the response
        result = {
            'friends': [
                {
                    'friend_id': friend.user1_id if friend.user1_id != user_id else friend.user2_id,
                    'friend_name': User.query.get(friend.user1_id).username if friend.user1_id != user_id else User.query.get(friend.user2_id).username,
                    'friend_email': User.query.get(friend.user1_id).email if friend.user1_id != user_id else User.query.get(friend.user2_id).email,
                    'friend_profile_pic': User.query.get(friend.user1_id).profile_pic if friend.user1_id != user_id else User.query.get(friend.user2_id).profile_pic,
                }
                for friend in friends_results
            ],
        }

        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)}) 



@main.route('/get_playlists_songs/<playlistID1>/<playlistID2>')
def get_playlists_songs(playlistID1, playlistID2):
    sp = spotipy.Spotify(auth=token)  # token, geçerli bir Spotify API erişim tokeni olmalıdır

    all_songs = []

    # Her iki playlist için şarkıları sorgula ve birleştir
    for playlist_id in [playlistID1, playlistID2]:
        playlist_tracks = sp.playlist_tracks(playlist_id)

        for track in playlist_tracks['items']:
            track_data = track['track']
            song_data = {
                'artist_name': track_data['artists'][0]['name'],
                'song_name': track_data['name'],
                'song_id': track_data['id'],
                'picture': track_data['album']['images'][0]['url'],
                'songLength': track_data['duration_ms'],
            }
            all_songs.append(song_data)

    return jsonify(all_songs) 
