from flask import Flask, request, url_for, redirect, session, jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS, cross_origin
from spotipy.oauth2 import SpotifyOAuth 
import spotipy
import requests


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
        redirect_uri=url_for("redirect_page", _external=True),
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

@app.route('/login_spotify')
def login_spotify():
    auth_url = create_spotify_outh().get_authorize_url()
    return redirect(auth_url)

@app.route('/sign_up', methods=['POST', 'GET'])
def sign_up():
    if request.method == "POST":
        data = request.get_json()
        
        cur = mysql.connection.cursor()
        
        # Create the User table if it doesn't exist
        cur.execute(user_table_query)
        
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


@app.route("/redirect_page")
def redirect_page():
    session.clear()
    code = request.args.get("code")
    token_info = create_spotify_outh().get_access_token(code)
    session[TOKEN_INFO] = token_info
    
    spotify = spotipy.Spotify(auth=token_info['access_token'])
    user_data = spotify.current_user()
    
    cur = mysql.connection.cursor()
    
    update_query = """
        UPDATE `User`
        SET `spotifyid` = %s, `country` = %s
        WHERE `email` = %s
    """
    cur.execute(update_query, (user_data["id"], user_data["country"], user_data["email"]))
    
    return user_data  


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8008, debug=True)