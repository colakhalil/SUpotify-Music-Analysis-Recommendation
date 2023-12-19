from flask import Blueprint, Flask, request, url_for, session, jsonify, redirect
from flask_cors import CORS, cross_origin
from spotipy.oauth2 import SpotifyOAuth 
from sqlalchemy import or_
from sqlalchemy.orm import aliased
import spotipy
import requests
import time 
import json
from . import db 
from .models import Album, Friendship, RateSong, SongPlaylist, Playlist, Artist, Song, User

user = Blueprint('user', __name__)

TOKEN_INFO = "token_info" 

client_id = "e3bb122dc61347a6b496d5f15a036a68"
client_secret = "e217a887698a43479bcbcc3698853677"

@user.route('/user_data/<email>', methods=['GET'])
def user_page(email):
    
    user = User.query.filter_by(email=email).first()
    if user:
        user_info = {
            'user_id': user.user_id,
            'profile_pic': user.profile_pic,
            'last_sid': user.last_sid
        }
    else:
        return jsonify({'message': False})
    
    UserAlias = aliased(User)

    friends_query = (
        db.session.query(User.user_id)
        .join(Friendship, or_(Friendship.user1_id == User.user_id, Friendship.user2_id == User.user_id))
        .filter(or_(Friendship.user1_id == user_info['user_id'], Friendship.user2_id == user_info['user_id']))
    )

    friends = friends_query.all()
    
    return jsonify({
        'username': user.user_id,
        'profilePicture': user.profile_pic,
        'lastListenedSong': user.last_sid,
        'friends': friends,
        'friendsCount': len(friends)
    })

@user.route('/friends_activity/<user_id>', methods=['GET'])
def friends_activity(user_id):
    
    friends = Friendship.query.filter_by(user1_id=user_id).all()
    friends2 = Friendship.query.filter_by(user2_id=user_id).all()
    
    all_friends = []
    
    for friend in friends:
        all_friends.append(friend.user2_id)
        
    for friend in friends2:
        all_friends.append(friend.user1_id)
        
    return jsonify({
        'name': friend.user_id,
        'lastListenedSong': friend.last_sid,
        'profilePicture': friend.profile_pic
    }for friend in all_friends)

from sqlalchemy import func 
@user.route('/<user_id>/newSongs', methods=['GET'])
def get_user_new_songs(user_id):
    try:
        # Get the user based on the provided user_id
        user = User.query.get(user_id)

        if user:
            # Query to get songs released in the current year (2023)
            current_year_songs = (
                db.session.query(Song)
                .filter(func('year', Song.release_date) == 2023)
                .all()
            )

            print("DEBUG: current_year_songs:", current_year_songs)

            if not current_year_songs:
                return jsonify({'error': 'No songs found for the current year.'})

            # Format the response
            result = {
                'user_id': user_id,
                'current_year_songs': [
                    {
                        'song_id': song.song_id,
                        'song_name': song.song_name,
                        'artist_name': song.artist.artist_name,
                        'release_date': song.release_date,
                    }
                    for song in current_year_songs
                ],
            }

            return jsonify(result)
        else:
            return jsonify({'error': 'User not found.'}), 404

    except Exception as e:
        print("DEBUG: Exception:", str(e))
        return jsonify({'error': str(e)})


@user.route('/<user_id>/monthly_average_rating', methods=['GET'])
def get_user_monthly_average_rating(user_id):
    try:
        # Query to get the monthly average rating of songs by a user
        monthly_average_ratings = (
            db.session.query(
                func.extract('year', RateSong.timestamp).label('year'),
                func.extract('month', RateSong.timestamp).label('month'),
                func.avg(RateSong.rating).label('average_rating')
            )
            .filter(
                RateSong.user_id == user_id,
            )
            .group_by('year', 'month')
            .order_by('year', 'month')
            .all()
        )

        if not monthly_average_ratings:
            return jsonify({'error': 'No monthly average ratings found for the user.'})

        # Format the response
        result = {
            'user_id': user_id,
            'monthly_average_ratings': [
                {
                    'year': rating.year,
                    'month': rating.month,
                    'average_rating': rating.average_rating,
                }
                for rating in monthly_average_ratings
            ],
        }

        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)})
#####YENI E MAIL 
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
def send_email(receiver_address, subject, body):
    sender_address = 'supotifysabanci@gmail.com'
    sender_pass = 'njzq stga irtl irrp'
    server = smtplib.SMTP('smtp.gmail.com', 587)  # SMTP sunucu adresini ve portunu girin

    # SMTP sunucusuna bağlanma ve oturum açma
    server.starttls()
    server.login(sender_address, sender_pass)

    # E-posta içeriğini oluşturma
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    # E-posta gönderme ve bağlantıyı kapatma
    server.send_message(message)
    server.quit()
##mail icin  highly rated route
def most_rated_songs_mail(current_user_id):
    # Fetch the most recent highly-rated songs listened by the user
    recent_highly_rated_songs = (
        RateSong.query
        .filter(RateSong.user_id == current_user_id, RateSong.rating >= 4)
        .limit(20)
        .all()
    )
    
    # Recommendation based on highly-rated songs
    song_recommendations = []
    for song in recent_highly_rated_songs:
        song_info = Song.query.filter(Song.song_id == song.song_id).first()
        artists = ArtistsOfSong.query.filter(ArtistsOfSong.song_id == song.song_id).all()
        song_recommendations.append({
            'artists': [Artist.query.filter_by(artist_id=artist.artist_id).first().artist_name for artist in artists],
            'song_name': song_info.song_name, 
            'timestamp': song.timestamp,
            'rating': song.rating,
            'album_name': song_info.album.album_name,
            'picture': song_info.picture,
            'song_id': song.song_id,
            'album_id': song_info.album_id,
            'duration': song_info.duration
        })

    return str(song_recommendations)
@user.route('/send_recommendations/<user_id>', methods=['GET'])
@cross_origin()
def send_recommendations(user_id):
    try:
        # Kullanıcıyı ve tavsiye edilen şarkıları getirin
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404

        song_recommendations = most_rated_songs_mail(user_id)+ "\n"
        email_body = "Your song recommendations:\n" + song_recommendations + "love <3, \n SUpotify"

        # E-posta gönder
        send_email(user.email, "Song Recommendations", email_body)

        return jsonify({'message': 'Recommendations sent successfully!'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500
   
