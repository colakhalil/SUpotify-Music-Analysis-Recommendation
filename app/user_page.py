from flask import Blueprint, Flask, request, url_for, session, jsonify, redirect
from flask_cors import CORS, cross_origin
from spotipy.oauth2 import SpotifyOAuth 
from sqlalchemy import or_, func
from sqlalchemy.orm import aliased
import spotipy
import requests
import time 
import json
from . import db 
from .models import Album, Friendship, RateSong, SongPlaylist, Playlist, Artist, Song, User

user = Blueprint('user', __name__)

TOKEN_INFO = "token_info" 

#WORKS
@user.route('/user_data/<email>', methods=['GET'])
@cross_origin()
def user_page(email):
    
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'message': False})

    user_id = user.user_id
    
    friends1 = Friendship.query.filter_by(user1_id=user_id).all()
    
    friends2 = Friendship.query.filter_by(user2_id=user_id).all()
    
    friends = []
    
    for friend in friends1:
        friends.append(friend.user2_id)
    
    for friend in friends2:
        friends.append(friend.user1_id)
        
    
    return jsonify({
        'username': user_id,
        'profilePicture': user.profile_pic,
        'lastListenedSong': user.last_sid,
        'friends': friends,
        'friendsCount': len(friends)
    })


#WORKS
@user.route('/friends_activity/<user_id>', methods=['GET'])
@cross_origin()
def friends_activity(user_id):
    
    friends = Friendship.query.filter_by(user1_id=user_id).all()
    friends2 = Friendship.query.filter_by(user2_id=user_id).all()
    
    all_friends = []
    
    to_be_returned = []
    
    for friend in friends:
        all_friends.append(friend.user2_id)
        
    for friend in friends2:
        all_friends.append(friend.user1_id)
        
    for friend in all_friends:
        user = User.query.filter_by(user_id=friend).first()
        to_be_returned.append({
            'name': user.user_id,
            'profilePicture': user.profile_pic,
            'lastListenedSong': user.last_sid
        })
        
    return jsonify(to_be_returned)

#WILL BE CHECKED AFTER DATABASE IS FILLED WITH RATING DATA
@user.route('/<user_id>/monthly_average_rating', methods=['GET'])
@cross_origin()
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

#WORKS
@user.route('/add_friend/<user_id>', methods=['POST'])
@cross_origin()
def add_friend(user_id):
    friend_id = request.json.get('friend_id')

    user = User.query.get(user_id)
    friend = User.query.get(friend_id)

    if not user:
        return jsonify({'error': 'User not found'})

    if not friend:
        return jsonify({'error': 'Friend not found'})

    if Friendship.query.filter(
            ((Friendship.user1_id == user_id) & (Friendship.user2_id == friend_id)) |
            ((Friendship.user1_id == friend_id) & (Friendship.user2_id == user_id))
    ).first():
        return jsonify({'error': 'Already friends'})

    new_friendship = Friendship(user1_id=user_id, user2_id=friend_id)

    db.session.add(new_friendship)
    db.session.commit()

    return jsonify({'message': 'Friend added successfully'})

@user.route('/remove_friend/<user_id>', methods=['POST'])
@cross_origin()
def remove_friend(user_id):
    friend_id = request.json.get('friend_id')

    user = User.query.get(user_id)
    friend = User.query.get(friend_id)

    if not user:
        return jsonify({'error': 'User not found'})

    if not friend:
        return jsonify({'error': 'Friend not found'})

    existing_friendship = Friendship.query.filter(
        ((Friendship.user1_id == user_id) and (Friendship.user2_id == friend_id)) or
        ((Friendship.user1_id == friend_id) and (Friendship.user2_id == user_id))
    ).first()

    if not existing_friendship:
        return jsonify({'error': 'Not friends'})

    db.session.delete(existing_friendship)
    db.session.commit()

    return jsonify({'message': 'Friend removed successfully'})

@user.route('/search_user/<search_term>', methods=['GET'])
@cross_origin()
def search_friends(search_term):
    users = User.query.filter(User.user_id.like(f'%{search_term}%')).all()
    if not users:
        return jsonify({'error': 'No users found'})

    return jsonify([{'user_id': user.user_id, 'profile_pic': user.profile_pic} for user in users])