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
 