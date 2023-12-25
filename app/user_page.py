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
from .models import Album, Friendship, RateSong, SongPlaylist, Playlist, Artist, Song, User, ArtistsOfSong

user = Blueprint('user', __name__)

TOKEN_INFO = "token_info" 
# Route to retrieve user data by email
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
    
@user.route('/user_data_username/<user_id>', methods=['GET'])
@cross_origin()
def user_page_username(user_id):
    
    user = User.query.filter_by(user_id=user_id).first()
    if not user:
        return jsonify({'message': False})
    
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


# Route to retrieve the activity of friends of a given user
@user.route('/friends_activity/<user_id>', methods=['GET'])
@cross_origin()
def friends_activity(user_id):
    
    friends = Friendship.query.filter_by(user1_id=user_id).all()
    friends2 = Friendship.query.filter_by(user2_id=user_id).all()
    
    all_friends = []
    
    to_be_returned = []
    
    for friend in friends:
        all_friends.append({
            "user_id": friend.user2_id,
            "rate_sharing": friend.rate_sharing
        })
        
    for friend in friends2:
        all_friends.append({
            "user_id": friend.user1_id,
            "rate_sharing": friend.rate_sharing
        })
        
    for friend in all_friends:
        user = User.query.filter_by(user_id=friend["user_id"]).first()
        if friend["rate_sharing"] == "public":
            to_be_returned.append({
                'name': user.user_id,
                'profilePicture': user.profile_pic,
                'lastListenedSong': user.last_sid
            })
        else:
            to_be_returned.append({
                'name': user.user_id,
                'profilePicture': user.profile_pic,
                'lastListenedSong': "private"
            })
        
    return jsonify(to_be_returned)

# Route to calculate the monthly average rating of songs by a user 
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

# Route to add a friend for a user 
@user.route('/add_friend/<user_id>', methods=['POST'])
@cross_origin()
def add_friend(user_id):
    friend_id = request.json.get('friend_id')
    rate_sharing = request.json.get('rate_sharing', 'private')  # Default to 'private' if not provided

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

    new_friendship = Friendship(user1_id=user_id, user2_id=friend_id, rate_sharing=rate_sharing)

    db.session.add(new_friendship)
    db.session.commit()

    return jsonify({'message': 'Friend added successfully'})

# Route to search for users based on a search term
@user.route('/search_user/<search_term>', methods=['GET'])
@cross_origin()
def search_friends(search_term):
    users = User.query.filter(User.user_id.like(f'%{search_term}%')).all()
    if not users:
        return jsonify({'error': 'No users found'})

    return jsonify([{'user_id': user.user_id, 'profile_pic': user.profile_pic} for user in users])
# Route to remove a friend from a user's friend list
@user.route('/remove_friend/<user_id>', methods=['POST'])
@cross_origin()
def remove_friend(user_id):
    friend_id = request.json.get('friend_id')

    user = User.query.filter_by(user_id=user_id).first()
    friend = User.query.filter_by(user_id=friend_id).first()

    if not user:
        return jsonify({'error': 'User not found'})

    if not friend:
        return jsonify({'error': 'Friend not found'})

    existing_friendship = Friendship.query.filter(
        ((Friendship.user1_id == user_id) & (Friendship.user2_id == friend_id)) |
        ((Friendship.user1_id == friend_id) & (Friendship.user2_id == user_id))
    ).first()

    if not existing_friendship:
        return jsonify({'error': 'Not friends'})

    db.session.delete(existing_friendship)
    db.session.commit()

    return jsonify({'message': 'Friend removed successfully'})

# Route to fetch the most rated songs by the current user
@user.route('/<current_user_id>/most_rated_songs', methods=['GET'])
@cross_origin()
def most_rated_songs(current_user_id):
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

    return jsonify({'most_rated_songs': song_recommendations})
    
# Route to update the friendship settings, like rate sharing preference 
@user.route('/update_friendship/<user_id>', methods=['POST'])
@cross_origin()
def update_friendship(user_id):
    try:
        data = request.get_json()
        friend_id = data.get('friend_id')
        new_rate_sharing = data.get('rate_sharing')

        friendship = Friendship.query.filter(
            ((Friendship.user1_id == user_id) & (Friendship.user2_id == friend_id)) |
            ((Friendship.user1_id == friend_id) & (Friendship.user2_id == user_id))
        ).first()

        if friendship:
            friendship.rate_sharing = new_rate_sharing
            db.session.commit()
            return jsonify({"message": "Friendship rate_sharing updated successfully."})
        else:
            return jsonify({"message": "Friendship not found."}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500
# Route to retrieve all rated songs by the current user     
@user.route('/<current_user_id>/all_rated_songs', methods=['GET'])
@cross_origin()
def all_rated_songs(current_user_id):
    # Fetch the most recent highly-rated songs listened by the user
    recent_highly_rated_songs = (
        RateSong.query
        .filter(RateSong.user_id == current_user_id, RateSong.rating >= 3)
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
            'rating': song.rating,
            'album_name': song_info.album.album_name,
            'picture': song_info.picture,
            'song_id': song.song_id,
            'album_id': song_info.album_id,
            'songLength': song_info.duration
        })

    return jsonify(song_recommendations)
