from collections import Counter
from flask import Blueprint, Flask, request, url_for, session, jsonify, redirect
from flask_cors import CORS, cross_origin
from spotipy.oauth2 import SpotifyOAuth 
from sqlalchemy import func, or_, desc
from threading import Thread
import lyricsgenius as lg
import spotipy
import requests
import time 
import json
from datetime import datetime
from . import db 
from .models import Album, Friendship, RateSong, SongPlaylist, Playlist, Artist, Song, User, RateArtist, RateAlbum, ArtistsOfSong
from datetime import datetime

main = Blueprint('main', __name__)

TOKEN_INFO = "token_info" 

token = ""

GENIUS_API_KEY = "ELYRzAgCM0wR2jm42T8YVN3sJZMXH4Yss-hBIERYV4xFp2RJGiRbrfnuQh5gqJfg"

# Function to fetch and save song information from Spotify
def fetch_and_save_song(sp, song_id):
    
    track_info = sp.track(song_id)
    
    audio_features = sp.audio_features(song_id)[0]
    
    artist = sp.artist(track_info['artists'][0]['id'])
    
    album = sp.album(track_info['album']['id'])
    
    genres = ', '.join(artist['genres'])
    
    new_artist = None
    
    new_album = None
    
    all_artists_list = track_info['artists']
    for singer in all_artists_list:
        artist_info = sp.artist(singer['id'])
        if not Artist.query.filter_by(artist_id=singer['id']).first():
            new_artist = Artist(
                artist_id = singer['id'],
                artist_name = singer['name'],
                picture = artist_info['images'][0]['url'],
                popularity = artist_info['popularity'],
                genres = genres,
                followers = artist_info['followers']['total']
            )
            db.session.add(new_artist)
        new_song_artist = ArtistsOfSong(song_id=track_info['id'], artist_id=singer['id'])
        db.session.add(new_song_artist)
        
    if not Album.query.filter_by(album_id=album['id']).first():
        new_album = Album(
            album_name = album['name'],
            album_id = album['id'],
            artist_id = artist['id'],
            album_type = album['album_type'],
            image = album['images'][0]['url']
        )
        db.session.add(new_album)
    
    release_year = int(track_info['album']['release_date'][:4])
    
    new_song = Song(
                song_id = track_info['id'],
                artist_id = track_info['artists'][0]['id'],
                album_id = track_info['album']['id'],
                song_name = track_info['name'],
                picture = track_info['album']['images'][0]['url'],
                play_count = 0,
                tempo = audio_features['tempo'],  
                popularity = track_info['popularity'],
                valence = audio_features['valence'],  
                duration = track_info['duration_ms'],
                energy = audio_features['energy'],  
                danceability = audio_features['danceability'],
                genre = genres,
                release_date = release_year,
                date_added = datetime.now(),
                artist = Artist.query.filter_by(artist_id=artist['id']).first() if Artist.query.filter_by(artist_id=artist['id']).first() else new_artist,
                album = Album.query.filter_by(album_id=album['id']).first() if Album.query.filter_by(album_id=album['id']).first() else new_album
            )
    
    db.session.add(new_song)
    db.session.commit()
    
# Route to store Spotify token information
@main.route('/token_add')
@cross_origin()
def token_add():
    global token
    token = session['token_info']['access_token']
    return redirect("http://localhost:3000/main")

# Mobile version of the token add route
@main.route('/token_add_mobile')
@cross_origin()
def token_add_mobile():
    global token
    token = session['token_info']['access_token']
    return "SUCCESS"

# Route to fetch lyrics of a song using the Genius API 
@main.route("/lyrics/<artist_name>/<song_name>")
@cross_origin()
def lyrics(artist_name, song_name):
    
    #DB check must be done here
    
    genius = lg.Genius(GENIUS_API_KEY)
    song = genius.search_song(title = song_name, artist = artist_name)
    
    return jsonify(song.lyrics)
    
# Route to save a song to the database 
@main.route('/save_song/<song_id>', methods=['GET', 'POST'])
@cross_origin()
def save_song(song_id):
    if request.method == 'GET':
        
        sp = spotipy.Spotify(auth=token)     
        
        fetch_and_save_song(sp, song_id)
        
        song = Song.query.filter_by(song_id=song_id).first()
        
        artists = ArtistsOfSong.query.filter_by(song_id=song_id).all()
        
        return jsonify({
            "name":song.song_name,
            "artists":[Artist.query.filter_by(artist_id=artist.artist_id).first().artist_name for artist in artists]
            })

# Route to get recommendations based on genre from Spotify
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
        songs = Song.query.all()
        db_result = []
        for song in songs:
            if genre in song.genre:
                db_song = {
                    'song_id': song.song_id,
                    'song_name': song.song_name,
                    'artist_name': song.artist.artist_name if song.artist else '',
                    'picture': song.picture,
                    'songLength': song.duration,
                }
                db_result.append(db_song)
        return jsonify(db_result)

# Route to fetch and save song information, or retrieve existing song information
@main.route('/get_song_info/<user_id>/<song_id>') 
@cross_origin()
def get_song_info(user_id, song_id):
    song = Song.query.filter_by(song_id=song_id).first()
   
    if not song:
        sp = spotipy.Spotify(auth=token) 
        fetch_and_save_song(sp, song_id)
        
    song = Song.query.filter_by(song_id=song_id).first()
    prev_rate = RateSong.query.filter_by(song_id=song_id, user_id=user_id).first()
    prev_rate_album = RateAlbum.query.filter_by(album_id=song.album_id, user_id=user_id).first()
    artists = ArtistsOfSong.query.filter_by(song_id=song_id).all()
    prev_rate_artist = RateArtist.query.filter_by(artist_id=song.artist_id, user_id=user_id).first()

    song_info = {
        'song_id': song.song_id,
        "artist_id": song.artist_id,
        "album_id": song.album_id,
        'artists': [Artist.query.filter_by(artist_id=artist.artist_id).first().artist_name for artist in artists],
        'title': song.song_name,
        'thumbnail': song.picture,
        'playCount': song.play_count,
        'popularity': song.popularity,
        'valence': song.valence,
        'duration': song.duration,
        'genre': song.genre,
        'releaseYear': song.release_date,
        'dateAdded': song.date_added,
        'userPrevRating': prev_rate.rating if prev_rate else 0,
        'userPrevRatingAlbum': prev_rate_album.rating if prev_rate_album else 0,
        'userPrevRatingArtist': prev_rate_artist.rating if prev_rate_artist else 0,
    }


    return jsonify(song_info)

# Route to fill the database with songs from a specified playlist 
@main.route('/fill_db/<playlist_id>')
@cross_origin()
def fill_db(playlist_id):
    sp = spotipy.Spotify(auth=token)
    playlist_added = sp.playlist_tracks(playlist_id)
    counter = 0
    for track in playlist_added['items']:
        track_info = track['track']

        existing_track = Song.query.filter_by(song_id=track_info['id']).first()

        if not existing_track:
            fetch_and_save_song(sp, track_info['id'])

        new_rate = RateSong(
            song_id=track_info['id'],
            user_id="yeren",
            rating= counter % 5,
            timestamp = datetime(2023, counter % 12 + 1, 1)
        )
        
        db.session.add(new_rate)
        counter += 1
        
    db.session.commit()

    return jsonify({'message': "DB FILLED!"})

# Route to get the user's playlists from Spotify 
@main.route('/get_user_playlists')
@cross_origin()
def get_user_playlists():
    
    sp = spotipy.Spotify(auth=token)
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

        if not existing_playlist:
            new_playlist = Playlist(
                playlist_id=playlist_data['playlistID'],
                playlist_name=playlist_data['name'],
                picture=playlist_data["playlistPic"],
                song_number=playlist_data['songNumber']
            )
            db.session.add(new_playlist)
            
    db.session.commit()

    return jsonify(formatted_playlists) 

# Route to change the rating of a song
@main.route('/change_rating_song', methods=['GET', 'POST'])
@cross_origin()
def change_rating_song():
    if request.method == 'POST':
        data = request.get_json()
        prev_rate = RateSong.query.filter_by(song_id=data['song_id'], user_id=data['user_id']).first()
        if ((data['rating'] < 0) or (data['rating'] > 5)):
            return jsonify({'message': False})
        if prev_rate:
            RateSong.query.filter_by(song_id=data['song_id'], user_id=data['user_id']).update({'rating': data['rating'], 'timestamp': datetime.now()})
        else:
            new_rate = RateSong(
                song_id=data['song_id'],
                user_id=data['user_id'],
                rating=data['rating']
            )
            db.session.add(new_rate)
     
        db.session.commit()
        
        return jsonify({'message': True})
    
# Route to update song play count
@main.route('/song_played', methods=['GET', 'POST'])
@cross_origin()
def song_played():
    if request.method == 'POST':
        data = request.get_json()
        song = Song.query.filter_by(song_id=data['song_id']).first()
        if song:
            User.query.filter_by(user_id=data['user_id']).update({'last_sid': song.song_id})
            Song.query.filter_by(song_id=data['song_id']).update({'play_count': song.play_count + 1})
            db.session.commit()
            return jsonify({'message': True})
        else:
            return jsonify({'message': False})
        
# Route to get detailed information of a specific playlist 
@main.route("/get_playlist_info/<user_id>/<playlist_id>")
@cross_origin()
def get_playlist_info(user_id,playlist_id):
    sp = spotipy.Spotify(auth=token)
    playlist_info = sp.playlist(playlist_id)
    song_list = []
 
    for i in range(len(playlist_info['tracks']['items'])):  
        
        s = RateSong.query.filter_by(song_id=playlist_info['tracks']['items'][i]['track']['id']).filter_by(user_id=user_id).first()
        
        song_1 = {
            'song_id' : playlist_info['tracks']['items'][i]['track']['id'],
            'song_name' : playlist_info['tracks']['items'][i]['track']['name'],
            'duration' : playlist_info['tracks']['items'][i]['track']['duration_ms'],
            'release_year' : playlist_info['tracks']['items'][i]['track']['album']['release_date'],
            'artist' : playlist_info['tracks']['items'][i]['track']['artists'][0]['name'],
            'song_rating' : s.rating if s else 0
        }

        song_list.append(song_1) 
    data = {
        'playlistID': playlist_id,
        'playlistName': playlist_info['name'],
        'playlistPicture': playlist_info['images'][0]['url'],
        'songs' : song_list
        }
    
    return jsonify(data)

# Route to save a song with form data
@main.route("/save_song_with_form", methods=['GET', 'POST'])
@cross_origin()
def save_song_with_form():
    if request.method == 'POST':
        
        data = request.get_json()
        
        artist = Artist.query.filter_by(artist_name=data['artistName']).first()
        
        if not artist:
                
            artist = Artist(
                artist_id = data['artistName'],
                artist_name = data['artistName'],
                picture = "unknown",
                genres = data['songGenre']
            )
            db.session.add(artist)


        new_song = Song(
                song_id = f"{data['artistName']}-{data['songTitle']}",
                artist_id = artist.artist_id,
                album_id = "unknown",
                song_name = data['songTitle'],
                play_count = 0,
                duration = data['songDuration'],
                genre = data['songGenre'],
                release_date = data['songReleaseYear'],
                artist = artist
            )
        
        db.session.add(new_song)
        db.session.commit()
        
        return jsonify({'message': True})
    
# Route to get highly rated 90s songs for a specific user
@main.route('/<user_id>/90s', methods=['GET'])
@cross_origin()
def get_user_highly_rated_90s_songs(user_id):
    try:
        # Query to get all songs from the 90s
        songs_90s = Song.query.filter(Song.release_date >= 1990, Song.release_date < 2000).all()
        
        # Query to get the user-specific rate for each song
        user_rates = RateSong.query.filter(RateSong.user_id == user_id).all()
        user_rates_dict = {rate.song_id: rate.rating for rate in user_rates}
        
        # Filter songs with user ratings and sort them based on the rating
        sorted_songs = sorted(
            (song for song in songs_90s if song.song_id in user_rates_dict),
            key=lambda song: user_rates_dict[song.song_id],
            reverse=True
        )
        
        # Format the response
        result = {
            'user_id': user_id,
            'highly_rated_90s_songs': [
                {
                    'title': song.song_name,
                    'artist': [Artist.query.filter_by(artist_id=artist.artist_id).first().artist_name for artist in ArtistsOfSong.query.filter_by(song_id=song.song_id).all()],
                    'releaseYear': song.release_date,
                    'rate': user_rates_dict[song.song_id]
                }
                for song in sorted_songs
            ]
        }
        return jsonify(result)
    except Exception as e:
        print(e)

# Route to get all songs for a specific user
@main.route('/<user_id>/all_songs', methods=['GET'])
@cross_origin()
def get_all_songs(user_id):
    try:
        all_songs = Song.query.all()
        
        songs_returned = []
        
        for song in all_songs:
            rate = RateSong.query.filter_by(song_id=song.song_id, user_id=user_id).first()
            artists = ArtistsOfSong.query.filter_by(song_id=song.song_id).all()
            result = {
                'song_id': song.song_id,
                'artist_id': song.artist_id,
                'artist_name': [Artist.query.filter_by(artist_id=artist.artist_id).first().artist_name for artist in artists],
                'album_name': song.album.album_name if song.album else None,
                'song_name': song.song_name,
                'picture': song.picture,
                'rate': rate.rating if rate else 0,
                'tempo': song.tempo,
                'popularity': song.popularity,
                'valence': song.valence,
                'duration': song.duration,
                'energy': song.energy,
                'danceability': song.danceability,
                'genre': song.genre,
                'release_date': song.release_date,
                'play_count': song.play_count,
                'date_added': song.date_added.isoformat()
            }
            
            songs_returned.append(result)

        return jsonify({'songs': songs_returned})

    except Exception as e:
        return jsonify({'error': str(e)})

# Route to get new songs for a specific user
@main.route('/<user_id>/new_songs', methods=['GET'])
@cross_origin()
def get_user_new_songs(user_id):
    try:
        # Query to get songs released in the current year (2023)
        current_year_songs = Song.query.filter(Song.release_date == 2023).all()

        if not current_year_songs:
            return jsonify({'error': 'No songs found for the current year.'})

        result = []
        
        for song in current_year_songs:
            rate = RateSong.query.filter_by(song_id=song.song_id, user_id=user_id).first()
            artists = ArtistsOfSong.query.filter_by(song_id=song.song_id).all()
            curr_song = {
                'song_id': song.song_id,
                'song_name': song.song_name,
                'artist_name': [Artist.query.filter_by(artist_id=artist.artist_id).first().artist_name for artist in artists],
                'release_date': song.release_date,
                'rate': rate.rating if rate else 0
            }
            result.append(curr_song)

        

        return jsonify(result)

    except Exception as e:
        print("DEBUG: Exception:", str(e))
        return jsonify({'error': str(e)})

# Route to count songs for each artist
@main.route('/<user_id>/artist_song_count', methods=['GET'])
@cross_origin()
def artist_song_count(user_id):
    try:
        # Query to get the number of songs for each artist
        artist_song_counts = (
            db.session.query(
                ArtistsOfSong.artist_id,
                Artist.artist_name,
                func.count(ArtistsOfSong.song_id).label('song_count')
            )
            .join(Artist, ArtistsOfSong.artist_id == Artist.artist_id)
            .group_by(ArtistsOfSong.artist_id, Artist.artist_name)
            .order_by(func.count(ArtistsOfSong.song_id).desc())  # Order by song count in descending order
            .limit(10)  # Limit the result to the first 10 artists
            .all()
        )
        result = []
        
        for artist_id, artist_name, song_count in artist_song_counts:
            rate = RateArtist.query.filter_by(artist_id=artist_id, user_id=user_id).first()
            curr_artist = {
                'artist_name': artist_name,
                'song_count': song_count,
                'rate': rate.rating if rate else 0
            }
            result.append(curr_artist)
        # Format the response


        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)})

# Route to search items (songs, albums, artists) based on a term
@main.route('/search_item/<user_id>/<search_term>', methods=['GET'])
@cross_origin()
def search_item(user_id, search_term):
    try:
        # Search for songs, albums, artists, and friends in the database based on the search term
        song_results = Song.query.filter(Song.song_name.ilike(f"%{search_term}%")).all()
        album_results = Album.query.filter(Album.album_name.ilike(f"%{search_term}%")).all()
        artist_results = Artist.query.filter(Artist.artist_name.ilike(f"%{search_term}%")).all()
        
        result = {
            'songs': [
                {
                    'song_id': song.song_id,
                    'song_name': song.song_name,
                    'artist_name': [Artist.query.filter_by(artist_id=artist.artist_id).first().artist_name for artist in ArtistsOfSong.query.filter_by(song_id=song.song_id).all()],
                    'picture': song.picture,
                    'release_date': song.release_date,
                    'rate': RateSong.query.filter_by(song_id=song.song_id, user_id=user_id).first().rating if RateSong.query.filter_by(song_id=song.song_id, user_id=user_id).first() else 0
                }
                for song in song_results
            ],
            'albums': [
                {
                    'album_id': album.album_id,
                    'album_name': album.album_name,
                    'artist_name': Artist.query.filter_by(artist_id=album.artist_id).first().artist_name,
                    'image': album.image,
                    'rate': RateAlbum.query.filter_by(album_id=album.album_id, user_id=user_id).first().rating if RateAlbum.query.filter_by(album_id=album.album_id, user_id=user_id).first() else 0
                }
                for album in album_results
            ],
            'artists': [
                {
                    'artist_id': artist.artist_id,
                    'picture': artist.picture,
                    'artist_name': artist.artist_name,
                    'popularity': artist.popularity,
                    'rate': RateArtist.query.filter_by(artist_id=artist.artist_id, user_id=user_id).first().rating if RateArtist.query.filter_by(artist_id=artist.artist_id, user_id=user_id).first() else 0,
                }
                for artist in artist_results
            ],
     
        }

        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)})
        
# Route to save a song with a JSON file    
@main.route('/save_song_with_json', methods=['POST'])
@cross_origin()
def save_song_with_json():
    try:
        file = request.files['songs.json']
        json_data = file.read()
        data = json.loads(json_data)
        songs = data.get('songs', [])
        
        for song in songs:
            artist = Artist.query.filter_by(artist_name=song['artistName']).first()
            
            if not artist:
                
                artist = Artist(
                    artist_id = data['artistName'],
                    artist_name = data['artistName'],
                    picture = "unknown",
                    genres = data['songGenre']
                )
                db.session.add(artist)


            new_song = Song(
                    song_id = f"{data['artistName']}-{data['songTitle']}",
                    artist_id = artist.artist_id,
                    album_id = "unknown",
                    song_name = data['songTitle'],
                    play_count = 0,
                    duration = data['songDuration'],
                    genre = data['songGenre'],
                    release_date = data['songReleaseYear'],
                    artist = artist
                )
            
            db.session.add(new_song)
            
        db.session.commit()
            
        return jsonify({'message': True})
        
    
    except Exception as e:
        return jsonify({'error': str(e)})
    
# Route to change the rating of an artist
@main.route('/change_rating_artist', methods=['GET', 'POST'])
@cross_origin()
def change_rating_artist():
    if request.method == 'POST':
        data = request.get_json()
        prev_rate = RateArtist.query.filter_by(artist_id=data['artist_id'], user_id=data['user_id']).first()
        if ((data['rating'] < 0) or (data['rating'] > 5)):
            return jsonify({'message': False})
        if prev_rate:
            RateArtist.query.filter_by(artist_id=data['artist_id'], user_id=data['user_id']).update({'rating': data['rating'], 'timestamp': datetime.now()})
        else:
            new_rate = RateArtist(
                artist_id=data['artist_id'],
                user_id=data['user_id'],
                rating=data['rating']
            )
            db.session.add(new_rate)
        db.session.commit()
        
        return jsonify({'message': True})
    
# Route to change the rating of an album
@main.route('/change_rating_album', methods=['GET', 'POST'])
@cross_origin()
def change_rating_album():
    if request.method == 'POST':
        data = request.get_json()
        prev_rate = RateAlbum.query.filter_by(album_id=data['album_id'], user_id=data['user_id']).first()
        if ((data['rating'] < 0) or (data['rating'] > 5)):
            return jsonify({'message': False})
        if prev_rate:
            RateAlbum.query.filter_by(album_id=data['album_id'], user_id=data['user_id']).update({'rating': data['rating'], 'timestamp': datetime.now()})
        else:
            new_rate = RateAlbum(
                album_id=data['album_id'],
                user_id=data['user_id'],
                rating=data['rating']
            )
            db.session.add(new_rate)
        db.session.commit()
        
        return jsonify({'message': True})

# Route to get song recommendations based on friends' preferences 
@main.route('<current_user_id>/friends_recommendations', methods=['GET'])
@cross_origin()
def friends_recommendations(current_user_id):
    # Fetch the user's friends with rate_sharing preference
    friends = Friendship.query.filter(
        (Friendship.user1_id == current_user_id) | (Friendship.user2_id == current_user_id)
    ).all()

    # Filter friends based on rate_sharing preference
    friends_allowed_to_share_rate = [friend for friend in friends if friend.rate_sharing == 'public']

    friend_ids = set()
    for friend in friends_allowed_to_share_rate:
        friend_ids.add(friend.user1_id)
        friend_ids.add(friend.user2_id)

    # Fetch the top 20 songs rated by friends who allow rate sharing
    top_rated_songs = (
        RateSong.query.filter(RateSong.user_id.in_(friend_ids))
        .order_by(desc(RateSong.rating))
        .limit(20)
        .all()
    )

    # Get the details of the top-rated songs
    recommendations = []
    for rate_song in top_rated_songs:
        song = Song.query.get(rate_song.song_id)
        artists = ArtistsOfSong.query.filter_by(song_id=song.song_id).all()
        recommendations.append({
            'song_name': song.song_name,
            'artist_name': [Artist.query.filter_by(artist_id=artist.artist_id).first().artist_name for artist in artists],
            'rating': rate_song.rating,
            'song_id': song.song_id,
            'picture': song.picture,
            'songLength': song.duration
        })

    return jsonify({'recommendations': recommendations})

# Route to delete a song from the database 
@main.route('/<current_user_id>/friend_artist_recommendations', methods=['GET'])
def friend_artist_recommendations(current_user_id):
    # Fetch the user's friends
    friends = Friendship.query.filter(
        (Friendship.user1_id == current_user_id) | (Friendship.user2_id == current_user_id)
    ).all()

    friend_ids = set()
    for friend in friends:
        if friend.rate_sharing == 'public':
            friend_ids.add(friend.user1_id)
            friend_ids.add(friend.user2_id)

    # Fetch the most recent highly-rated songs listened by friends
    recent_highly_rated_songs = (
        RateArtist.query
        .filter(RateArtist.user_id.in_(friend_ids), RateArtist.rating >= 4)
        .order_by(desc(RateArtist.timestamp))
        .limit(20)
        .all()
    )

    # Get the unique artists from the highly-rated songs
    unique_artist_ids = set(song.artist_id for song in recent_highly_rated_songs)
    
    # Fetch the details of the unique artists
    artist_recommendations = []
    for artist_id in unique_artist_ids:
        artist = Artist.query.get(artist_id)
        if artist:
            artist_recommendations.append({
                'artist_name': artist.artist_name,
                'picture': artist.picture,
                'artist_id': artist.artist_id,
                'popularity': artist.popularity,
                'genres': artist.genres,
                'followers': artist.followers
            })

    return jsonify({'recommendations': artist_recommendations})
# Route to delete an song from the database 
@main.route('/delete_song/<song_id>', methods=['POST'])
@cross_origin()
def delete_song(song_id):

    song_to_delete = Song.query.filter_by(song_id=song_id).first()

    # Check if a song was found
    if song_to_delete:

        db.session.delete(song_to_delete)

        # Commit the changes to the database
        db.session.commit()

        return jsonify({"message": True})

    else:

        return jsonify({"message": False})
# Route to delete an album from the database 
@main.route('/delete_album/<album_id>', methods=['POST'])
@cross_origin()
def delete_album(album_id):

    album_to_delete = Album.query.filter_by(album_id=album_id).first()

    if album_to_delete:

        songs_to_delete = Song.query.filter_by(album_id=album_id).all()
        for song in songs_to_delete:
            db.session.delete(song)

        db.session.delete(album_to_delete)

        db.session.commit()

        return jsonify({"message": True})

    else:

        return jsonify({"message": False})

# Route to delete an artist from the database 
@main.route('/delete_artist/<artist_id>', methods=['POST'])
@cross_origin()
def delete_artist(artist_id):

        artist_to_delete = Artist.query.filter_by(artist_id=artist_id).first()

        if artist_to_delete:
            artist_id = artist_to_delete.artist_id
            albums_to_delete = Album.query.filter_by(artist_id=artist_id).all()

            for album in albums_to_delete:
                db.session.delete(album)

            featured_songs_to_delete = ArtistsOfSong.query.filter_by(artist_id=artist_id).all()

            for song_artist in featured_songs_to_delete:
                song_id = song_artist.song_id
                song_to_delete = Song.query.filter_by(song_id=song_id).first()
                if song_to_delete:
                    db.session.delete(song_to_delete)
                db.session.delete(song_artist)

            db.session.delete(artist_to_delete)
            db.session.commit()
            return jsonify({"message": True})
        else:
            return jsonify({"message": False})
# Route to get song recommendations from a specific artist
@main.route('/<current_user_id>/recommended_artist_songs', methods=['GET'])
def recommended_artist_songs(current_user_id):
    # Fetch the most liked artist's ID using the find_most_liked_artist function
    most_liked_artist_id = find_most_liked_artist(current_user_id)

    if most_liked_artist_id:
        # Get information about the most liked artist
        most_liked_artist = Artist.query.get(most_liked_artist_id)

        if most_liked_artist:
            # Fetch songs of the most liked artist from Spotify
            sp = spotipy.Spotify(auth=token)
            results = sp.artist_top_tracks(most_liked_artist.artist_id, country='US')

            # Extract relevant information from the Spotify API response
            song_recommendations = []
            for track in results['tracks']:
                song_recommendations.append({
                    'artist_name': [artist['name'] for artist in track['artists']],
                    'song_name': track['name'],
                    'song_id': track['id'],
                    'picture': track['album']['images'][0]['url'],
                    'songLength': track['duration_ms'],
                })

            return jsonify({'song_recommendations': song_recommendations})
        else:
            return jsonify({'error': 'Most liked artist not found'}), 404
    else:
        return jsonify({'error': 'Most liked artist ID not found'}), 404

def find_most_liked_artist(user_id):
    recent_highly_rated_songs = (
        RateArtist.query
        .filter(RateArtist.user_id == user_id, RateArtist.rating >= 4)
        .limit(20)
        .all()
    )

    # Get the count of each artist in highly-rated songs
    artist_counter = Counter(song.artist_id for song in recent_highly_rated_songs)
    if artist_counter:
    # Find the most liked artist
        most_liked_artist_id = artist_counter.most_common(1)[0][0]

    return most_liked_artist_id
# Route to get song recommendations based on a newly rated song
@main.route('/<current_user_id>/newly_rating_recomendations', methods=['GET']) 
@cross_origin()
def get_newly_recommendations(current_user_id):    
    recently_rated_song = (
    RateSong.query
    .filter_by(user_id=current_user_id)
    .filter(RateSong.rating >= 4)  # Add this filter condition
    .order_by(desc(RateSong.timestamp))
    .first() 
)

    if recently_rated_song:
         
        return redirect(f"http://127.0.0.1:8008/recommendations_track/{recently_rated_song.song_id}")
 
    else:
        return jsonify({'recommendation': None})

# Route to get Spotify recommendations based on a specific track
@main.route('recommendations_track/<track_id>')
@cross_origin()
def get_recommendations_by_track(track_id):
    sp = spotipy.Spotify(auth=token)
    try:
        recommendations = sp.recommendations(seed_tracks=[track_id], limit=10)
        print("Recommendations API Response:", recommendations)  # Add this line for logging
        result = format_recommendations(recommendations)
        return jsonify(result)
    except Exception as e:
        print(f"Error during API request: {e}")
        return jsonify({'error': str(e)}), 500

def format_recommendations(recommendations):
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
    print("Formatted Recommendations:", result)  # Add this line for logging
    return result

@main.route('/get_top_songs/<country_name>', methods=['GET'])
@cross_origin()
def get_top_50_songs_of_country(country_name):
    # Create a Spotify client
    sp = spotipy.Spotify(auth=token)

    # Generate the playlist name
    playlist_name = f"Top 50 - {country_name}"

    # Search for the playlist
    result = sp.search(q=playlist_name, type='playlist', limit=1)
    if not result['playlists']['items']:
        return {'message': False}

    # Get the playlist ID
    playlist_id = result['playlists']['items'][0]['id']

    # Get the first 10 songs of the playlist
    tracks = sp.playlist_tracks(playlist_id, limit=10)
    songs = []
    for item in tracks['items']:
        track = item['track']
        curr_track = {
            'song_id': track['id'],
            'song_name': track['name'],
            'artist_name': [artist['name'] for artist in track['artists']],
            'picture': track['album']['images'][0]['url'] if track['album']['images'] else None,
            'songLength': track['duration_ms'],
        }
        songs.append(curr_track)

    return jsonify(songs)

@main.route('/enrich_rec/<user_id>/<genre>', methods=['GET'])
@cross_origin()
def enrich_rec(user_id, genre):

    songs = Song.query.filter(Song.genre.contains(genre)).all()
    result = []
    for song in songs:
        rate = RateSong.query.filter_by(song_id=song.song_id, user_id=user_id).first()
        artists = ArtistsOfSong.query.filter_by(song_id=song.song_id).all()
        curr_song = {
            'song_id': song.song_id,
            'song_name': song.song_name,
            'artist_name': [Artist.query.filter_by(artist_id=artist.artist_id).first().artist_name for artist in artists],
            'picture': song.picture,
            'songLength': song.duration,
            'release_date': song.release_date,
            'rate': rate.rating if rate else 0
        }
        result.append(curr_song)
    return jsonify(result)

@main.route('/get_playlists_songs/<playlistID1>/<playlistID2>')
@cross_origin()
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
