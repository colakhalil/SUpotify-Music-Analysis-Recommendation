from flask import Flask, request, url_for, redirect, session, jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS, cross_origin
from spotipy.oauth2 import SpotifyOAuth 
import spotipy
import requests
import time 
import json  


app = Flask(__name__)
app.config["SESSION_COOKIE_NAME"] = "spotify_cookie"
app.secret_key = "sdfsdf943urıjf0"

# Veritabanı bağlantısı oluşturma
app.config['MYSQL_HOST'] = 'db'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_PASSWORD'] = 'Atakan2002'
app.config['MYSQL_DB'] = 'flaskapp'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)
CORS(app, resources={
    r"/sign_up": {"origins": "http://localhost:3000"},
    r"/login": {"origins": "http://localhost:3000"}
})
# 'auth' Blueprint'ini kaydetme
#import auth  # Import 'auth' Blueprint
#app.register_blueprint(auth.auth, url_prefix='/auth')


TOKEN_INFO = "token_info" 

client_id = "e3bb122dc61347a6b496d5f15a036a68"
client_secret = "e217a887698a43479bcbcc3698853677"

# scope tanimi 
def create_spotify_outh():
    return SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=url_for("redirect_page", _external=True),  # Make sure this matches the registered redirect URI
        scope="user-read-playback-state user-read-private user-read-email user-follow-read user-top-read",
    )


"""@login_required  # make sure cannot go this page unless user is logged in 
def login_spotify():
    auth_url = auth.create_spotify_outh().get_authorize_url()

"""

user_table_query = """
CREATE TABLE IF NOT EXISTS `User` (
  `user_id` varchar(45) NOT NULL,
  `password` varchar(16) NOT NULL,
  `country` varchar(5) DEFAULT NULL,
  `spotifyid` varchar(45) DEFAULT NULL,
  `last_sid` varchar(45) DEFAULT NULL,
  `email` varchar(150) NOT NULL,
  PRIMARY KEY (`user_id`)
)"""

insert_user_query = """
INSERT INTO `User` (`user_id`, `password`, `email`)
VALUES (%s, %s, %s)
"""

select_user_query = "SELECT * FROM User" 

@app.route('/sign_up', methods=['POST', 'GET'])
def sign_up():
    if request.method == "POST":
        data = request.get_json()
        
        cur = mysql.connection.cursor()
        
        # Create the User table if it doesn't exist
        cur.execute(user_table_query)
        
        query = """SELECT * FROM User WHERE user_id = %s"""
        cur.execute(query, (data["user_id"],))
        db_data = cur.fetchone()
        
        if db_data:
            return jsonify({"message": "This user already exists"})
        
        # Insert user data into the User table
        cur.execute(insert_user_query, (data["user_id"], data["password"], data["email"]))
        mysql.connection.commit()
        
        cur.close()
        return jsonify({"message": "Success"})
        

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")
        
        cur = mysql.connection.cursor()
        query = """SELECT password FROM User WHERE email = %s"""
        cur.execute(query, (email,))
        user_data = cur.fetchone()
        cur.close()
        if user_data:
            if user_data["password"] == password:
                return jsonify({"message": "Success"})
            else:
                return jsonify({"message": "Wrong password"})
        else:
            return jsonify({"message": "This user does not exist"})

# spotify login 
@app.route('/')
def login_spotify():
    auth_url = create_spotify_outh().get_authorize_url()
    return redirect(auth_url)
 
@app.route("/redirect")
def redirect_page():
    session.clear()
    code = request.args.get("code")
    token_info = create_spotify_outh().get_access_token(code)
    session[TOKEN_INFO] = token_info
    
    spotify = spotipy.Spotify(auth=token_info['access_token'])
    user_data = spotify.current_user()
    
    #cur = mysql.connection.cursor()
    
    #update_query = """
    #    UPDATE `User`
    #   SET `spotifyid` = %s, `country` = %s
    #    WHERE `email` = %s
    #"""
    #cur.execute(update_query, (user_data["id"], user_data["country"], user_data["email"])) 
    print ("basarili.. ")
     
    return token_info 

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

@app.route('/recommendations/<genre>')
def get_recommendations_by_genre(genre):
    # Spotify API'yi kullanarak belirli bir tür için önerilen şarkıları al
    sp = spotipy.Spotify(auth=session[TOKEN_INFO]['access_token'])
    recommendations = sp.recommendations(seed_genres=[genre], limit=10)

    # Her şarkı için şarkı ve albüm bilgilerini çek
    for track in recommendations['tracks']:
        fetch_and_store_song_info(sp, track['id'])

    # Önerilen şarkıları template'e gönder
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

app.route('/get_song_info/<song_id>') 
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
        return jsonify(data)   
    
@app.route('/get_user_playlists')
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
 

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8008, debug=True)
