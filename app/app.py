import json
import time
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, jsonify, request, redirect, session, url_for


TOKEN_INFO = "token_info" 
app = Flask(__name__)
app.config["SESSION_COOKIE_NAME"] = "spotify_cookie"
app.secret_key = "sdfsdf943urıjf0"

client_id = "e3bb122dc61347a6b496d5f15a036a68"
client_secret = "e217a887698a43479bcbcc3698853677"

# scope tanimi 
def create_spotify_outh():
    return SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=url_for("redirect_page", _external=True),
        scope="user-read-playback-state user-read-private user-read-email user-follow-read user-top-read",
    )
 
@app.route("/")
def login():
    auth_url = create_spotify_outh().get_authorize_url()
    return redirect(auth_url)



@app.route("/redirect")
def redirect_page():
    session.clear()
    code = request.args.get("code")
    token_info = create_spotify_outh().get_access_token(code)
    session[TOKEN_INFO] = token_info  
    return  "basarili"




@app.route('/get_song_info/<song_id>') 
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
        'song_name': track_info['name'],
        'artist_id': track_info['artists'][0]['id'],
        'artist_name': track_info['artists'][0]['name'],	 
        'album_name': track_info['album']['name'],
        'album_id': track_info['album']['id'],
        'rate': None,  # Buraya isteğe bağlı bir değer ekleyebilirsiniz
        'tempo': None,  # Buraya isteğe bağlı bir değer ekleyebilirsiniz
        'popularity': track_info['popularity'],
        'valence': None,  # Buraya isteğe bağlı bir değer ekleyebilirsiniz  
        'duration': track_info['duration_ms'],  ## MILISECOND CINSINDEN VERIR !! 
        

    }
    
 
    
    return jsonify(data)

def get_token():
    token_info = session.get(TOKEN_INFO, None)
    if not token_info:  # Token doesn't exist
        return redirect(url_for("login", _external=False))
    now = int(time.time())
    is_expired = token_info["expires_at"] - now < 60
    if is_expired:
        spotify_oauth = create_spotify_outh()
        token_info = spotify_oauth.refresh_access_token(token_info["refresh_token"])
    return token_info["access_token"]


@app.route("/show_profile")
def show_profile():
    token = get_token()
    sp = spotipy.Spotify(auth=token)
    user_profile = sp.current_user()
    data = {
        'user_id': user_profile['id'],
        'user_name': user_profile['display_name'],
        'user_email': user_profile['email'],
        'user_country': user_profile['country'],
        'user_followers': user_profile['followers']['total'],
        

    } 

    # Process the user's profile data as needed
    return jsonify(data)

GENIUS_API_KEY = "ELYRzAgCM0wR2jm42T8YVN3sJZMXH4Yss-hBIERYV4xFp2RJGiRbrfnuQh5gqJfg"

## PIP INSTALL YAPTIMM !!!!!!! 
import lyricsgenius as lg

@app.route("/lyrics/<song_name>")
def lyrics(song_name):
    genius = lg.Genius(GENIUS_API_KEY)
    song = genius.search_song(title = song_name)
    return str(song.lyrics )
    
db = MySQLdb(app) 
app.route("/get_playlist_info/<playlist_id>")
def get_playlist_info(playlist_id):
    sp = spotipy.Spotify(auth=session['token_info']['access_token'])
    playlist_info = sp.playlist(playlist_id)
    song_list = []
    Song = namedtuple("Song", ["song_id", "song_name", "duration", "release_year", "artist", "song_rating"]) 

    cur = db.connection.cursor()
 
    for i in range(len(playlist_info['tracks']['items'])):  

        cur.execute("""
        SELECT `rate` FROM `Song` WHERE `song_id` = %s
    """, (playlist_info['tracks']['items'][i]['track']['id'],)) 
        s = cur.fetchone()  
        song_1 = Song(
            song_id = playlist_info['tracks']['items'][i]['track']['id'],
            song_name = playlist_info['tracks']['items'][i]['track']['name'],
            duration = playlist_info['tracks']['items'][i]['track']['duration_ms'],
            release_year = playlist_info['tracks']['items'][i]['track']['album']['release_date'],
            artist = playlist_info['tracks']['items'][i]['track']['artists'][0]['name'],
            song_rate = s 
        ) 
        song_list.append(song_1) 
    data = {
        'playlisID': playlist_id,
        'playlistName': playlist_info['name'],
        'playlistPicture': playlist_info['images'][0]['url'],
        'songs' : song_list,
        
        }  
    cur.close()
    return jsonify(data) 
 

app.run(debug=True, port=8080) 
 
