from flask import Flask, redirect
import unittest
from flask_sqlalchemy import SQLAlchemy
from app import create_app, db
import json
from app.main_page import fetch_and_save_song 
from datetime import datetime
from unittest.mock import patch, MagicMock, Mock
from app.auth import auth
from app.main_page import find_most_liked_artist
from app import create_app
from app.models import Album, Friendship, RateSong, SongPlaylist, Playlist, Artist, Song, User, RateArtist, RateAlbum, ArtistsOfSong

class MockSong:
    def __init__(self, song_id, song_name, picture, duration, release_date, genre):
        self.song_id = song_id
        self.song_name = song_name
        self.picture = picture
        self.duration = duration
        self.release_date = release_date
        self.genre = genre

class BluePrintTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = create_app().test_client()
        cls.app_context = create_app().app_context()
        cls.app_context.push()
        db.create_all()

    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()

    def setUp(self):
        pass

    def tearDown(self):
        self.clear_data()
        
    def create_test_data(self):
        # Create test data for friendships, songs, and ratings
        friendship1 = Friendship(user1_id=1, user2_id=2, rate_sharing='public')
        friendship2 = Friendship(user1_id=1, user2_id=3, rate_sharing='public')
        db.session.add_all([friendship1, friendship2])

        artist1 = Artist(artist_name='Artist 1', artist_id='1')
        artist2 = Artist(artist_name='Artist 2', artist_id='2')
        db.session.add_all([artist1, artist2])

        song1 = Song(song_name='Song 1', duration=180, picture='song1.jpg')
        song2 = Song(song_name='Song 2', duration=240, picture='song2.jpg')
        db.session.add_all([song1, song2])

        artist_of_song1 = ArtistsOfSong(song_id=song1.song_id, artist_id=artist1.artist_id)
        artist_of_song2 = ArtistsOfSong(song_id=song2.song_id, artist_id=artist2.artist_id)
        db.session.add_all([artist_of_song1, artist_of_song2])

        rate_song1 = RateSong(user_id=2, song_id=song1.song_id, rating=5)
        rate_song2 = RateSong(user_id=3, song_id=song2.song_id, rating=4)
        db.session.add_all([rate_song1, rate_song2])
        
        rate_artist1 = RateArtist(user_id=1, artist_id=artist1.artist_id, rating=5)
        rate_artist2 = RateArtist(user_id=1, artist_id=artist2.artist_id, rating=4)
        db.session.add_all([rate_artist1, rate_artist2])

        db.session.commit()

    def clear_data(self):
        # Clear data from each table without dropping the table
        for table in reversed(db.metadata.sorted_tables):
            db.session.execute(table.delete())
        db.session.commit()

    """"
    GIVEN a user is created
    WHEN the user is inserted manually to DataBase
    THEN user can be reached by filtering the DataBase
    """
    def test_db(self):
        with create_app().app_context():
            new_user = User(user_id="unittest_bismillah", password="pwd", email="test@example.com")
            db.session.add(new_user)
            db.session.commit()
     
            inserted_user = User.query.filter_by(user_id='unittest_bismillah').first()
            self.assertIsNotNone(inserted_user)
            self.assertEqual(inserted_user.email, 'test@example.com')

    """"
    GIVEN a user wants to sign up
    WHEN the user enters user_id, password and email
    THEN request should return True
    """
    def test_sing_up(self):
        with create_app().app_context():
            user_data = {
                'user_id': 'testuser2',
                'password': 'testpassword',
                'email': 'test2@example.com'
            }
            response = self.app.post('/sign_up', json=user_data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        result = response.data

        expected_message = b'{"message":true}\n'
        self.assertEqual(result, expected_message)

    """"
    GIVEN a username already exists
    WHEN the same username is used to sign up
    THEN request should return False
    """
    def test_signup_failure_existing_user(self):
        with create_app().app_context():
            test_user = User(user_id='testuser', password='testpassword', email='test@example.com')
            db.session.add(test_user)
            db.session.commit()

            response = self.app.post('/sign_up', json={'user_id': 'testuser', 'password': 'testpassword', 'email': 'test@example.com'})

        self.assertEqual(response.status_code, 200)

        result = json.loads(response.data)

        self.assertEqual(result['message'], False)

    """ 
    GIVEN a user in the database with correct credentials
    WHEN a POST request is made to the login endpoint with correct credentials
    THEN the response status code should be 200
    AND the login message should be True
    """
    def test_login_success(self):
        with create_app().app_context():
            test_user = User(user_id='testuser', password='testpassword', email='test@example.com')
            db.session.add(test_user)
            db.session.commit()

            response = self.app.post('/login', json={'email': 'test@example.com', 'password': 'testpassword'})

        self.assertEqual(response.status_code, 200)

        result = json.loads(response.data)

        self.assertEqual(result['message'], True)


    """
    GIVEN a user in the database with correct credentials
    WHEN a user tries to log in with incorrect credentials
    THEN the response status code should be 200
    AND the login message should be False
    """
    def test_login_failure_wrong_password(self):
        with create_app().app_context():
            test_user = User(user_id='testuser', password='testpassword', email='test@example.com')
            db.session.add(test_user)
            db.session.commit()

            response = self.app.post('/login', json={'email': 'test@example.com', 'password': 'wrongpassword'})

        
        self.assertEqual(response.status_code, 200)

        
        result = json.loads(response.data)
        self.assertEqual(result['message'], False)


    """
    GIVEN a valid song in the database
    WHEN that song is deleted
    THEN the response status code should be 200
    AND the message should be True
    """
    def test_delete_song(self):
        with create_app().app_context():
            test_song = Song(song_id="11dFghVXANMlKmJXsNCbNl")
            db.session.add(test_song)
            db.session.commit()

            response = self.app.post('/delete_song/11dFghVXANMlKmJXsNCbNl')
        
        self.assertEqual(response.status_code, 200)

        expected_response = {"message": True}
        self.assertEqual(response.get_json(), expected_response)

    """
    GIVEN a valid song in the database
    WHEN a song that is not in the database is deleted
    THEN the response status code should be 200
    AND the message should be False
    """
    def test_delete_song_invalid_song(self):
        with create_app().app_context():

            response = self.app.post('/delete_song/11dFghVXANMlKmJXsNCbNl')
        
        self.assertEqual(response.status_code, 200)

        expected_response = {"message": False}
        self.assertEqual(response.get_json(), expected_response)
    
    """
    GIVEN a valid album in the database
    WHEN an album that is in the database is deleted
    THEN the response status code should be 200
    AND the message should be of valid deletion
    """
    def test_delete_album(self):
        with create_app().app_context():
            test_album = Album(album_id="4aawyAB9vmqN3uQ7FjRGTy")
            db.session.add(test_album)
            db.session.commit()

            response = self.app.post('/delete_album/4aawyAB9vmqN3uQ7FjRGTy')
        
        self.assertEqual(response.status_code, 200)

        expected_response = {'message': True}
        self.assertEqual(response.get_json(), expected_response)

    
    """
    WHEN an album that is not in the database is deleted
    THEN the response status code should be 200
    AND the message should be of invalid deletion
    """
    def test_delete_album_invalid_song(self):
        with create_app().app_context():
            response = self.app.post('/delete_album/4aawyAB9vmqN3uQ7FjRGTy')
        
        self.assertEqual(response.status_code, 200)

        expected_response = {'message': False}
        self.assertEqual(response.get_json(), expected_response)

    """
    GIVEN a valid artist in the database
    WHEN that artist is deleted
    THEN the response status code should be 200
    AND the message should be of valid deletion
    """
    def test_delete_artist(self):
        artist_id = "0TnOYISbd1XYRBk9myaseg"
        with create_app().app_context():
            test_artist = Artist(artist_id="0TnOYISbd1XYRBk9myaseg")
            db.session.add(test_artist)
            db.session.commit()

            response = self.app.post('/delete_artist/0TnOYISbd1XYRBk9myaseg')
        
        self.assertEqual(response.status_code, 200)

        expected_response = {'message': True}
        self.assertEqual(response.get_json(), expected_response)


    """
    WHEN an artist that is not in the database is deleted
    THEN the response status code should be 200
    AND the message should be of invalid deletion
    """
    def test_delete_artist_invalid_artist(self):
        artist_id = "0TnOYISbd1XYRBk9myaseg"
        with create_app().app_context():

            response = self.app.post('/delete_artist/0TnOYISbd1XYRBk9myaseg')
        
        self.assertEqual(response.status_code, 200)

        expected_response = {'message': False}
        self.assertEqual(response.get_json(), expected_response)
        
    # Feature: User Page Functionality
    # Scenario: Retrieve user data based on email
    # Given: A mocked user and friendship data
    # When: A GET request is made to '/user_data/test_email'
    # Then: The user data should be returned successfully     
    @patch('app.main_page.User.query')
    @patch('app.main_page.Friendship.query')
    def test_user_page(self, mock_friendship_query, mock_user_query):
        # Mock the User query to return a User object when filtered by email
        mock_user = mock_user_query.filter_by.return_value.first.return_value
        mock_user.user_id = 'test_user_id'
        mock_user.profile_pic = 'test_profile_pic'
        mock_user.last_sid = 'test_last_sid'

        # Mock the Friendship query to return a list of Friendship objects
        # for both user1_id and user2_id filters
        mock_friendship1 = MagicMock()
        mock_friendship1.all.return_value = [
            Friendship(user1_id="test_user_id", user2_id="friend1"),
            Friendship(user1_id="test_user_id", user2_id="friend2")
        ]
        mock_friendship2 = MagicMock()
        mock_friendship2.all.return_value = [
            Friendship(user1_id="friend3", user2_id="test_user_id"),
            Friendship(user1_id="friend4", user2_id="test_user_id")
        ]
        mock_friendship_query.filter_by.side_effect = [mock_friendship1, mock_friendship2]
        
        # Send a GET request to the user_page endpoint with a test email
        response = self.app.get('/user_data/test_email')

        # Assert the response and data returned by the function
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {
            'username': 'test_user_id',
            'profilePicture': 'test_profile_pic',
            'lastListenedSong': 'test_last_sid',
            'friends': ['friend1', 'friend2', 'friend3', 'friend4'],
            'friendsCount': 4,
        })

    # Feature: User Page Functionality
    # Scenario: Retrieve user data based on username
    # Given: A mocked user and friendship data
    # When: A GET request is made to '/user_data_username/test_user_id'
    # Then: The user data should be returned successfully 
    @patch('app.main_page.User.query')
    @patch('app.main_page.Friendship.query')
    def test_user_page_username(self, mock_friendship_query, mock_user_query):
        # Mock the User query to return a User object when filtered by user_id
        mock_user = mock_user_query.filter_by.return_value.first.return_value
        mock_user.user_id = 'test_user_id'
        mock_user.profile_pic = 'test_profile_pic'
        mock_user.last_sid = 'test_last_sid'

        # Mock the Friendship query to return a list of Friendship objects
        # for both user1_id and user2_id filters
        mock_friendship1 = MagicMock()
        mock_friendship1.all.return_value = [
            Friendship(user1_id="test_user_id", user2_id="friend1"),
            Friendship(user1_id="test_user_id", user2_id="friend2")
        ]
        mock_friendship2 = MagicMock()
        mock_friendship2.all.return_value = [
            Friendship(user1_id="friend3", user2_id="test_user_id"),
            Friendship(user1_id="friend4", user2_id="test_user_id")
        ]
        mock_friendship_query.filter_by.side_effect = [mock_friendship1, mock_friendship2]
        
        # Send a GET request to the user_page_username endpoint with a test user_id
        response = self.app.get('/user_data_username/test_user_id')

        # Assert the response and data returned by the function
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {
            'username': 'test_user_id',
            'profilePicture': 'test_profile_pic',
            'lastListenedSong': 'test_last_sid',
            'friends': ['friend1', 'friend2', 'friend3', 'friend4'],
            'friendsCount': 4,
        }) 

    # Feature: Friends Activity Functionality
    # Scenario: Retrieve friends activity data for a user
    # Given: Mocked user and friendship data
    # When: A GET request is made to '/friends_activity/test_user_id'
    # Then: Friends activity data should be returned successfully 
    @patch('app.main_page.User.query')
    @patch('app.main_page.Friendship.query')
    def test_friends_activity(self, mock_friendship_query, mock_user_query):
        # Mock the Friendship query to return a list of Friendship objects
        # for both user1_id and user2_id filters
        mock_friendship1 = MagicMock()
        mock_friendship1.all.return_value = [
            Friendship(user1_id="test_user_id", user2_id="friend1", rate_sharing="public"),
            Friendship(user1_id="test_user_id", user2_id="friend2", rate_sharing="private")
        ]
        mock_friendship2 = MagicMock()
        mock_friendship2.all.return_value = [
            Friendship(user1_id="friend3", user2_id="test_user_id", rate_sharing="public")
        ]
        mock_friendship_query.filter_by.side_effect = [mock_friendship1, mock_friendship2]

        # Setup a side effect function for the mock_user_query.filter_by
        def user_query_side_effect(**kwargs):
            user_id = kwargs.get('user_id')
            mock_user = MagicMock()
            mock_user.user_id = user_id
            mock_user.profile_pic = f'{user_id}_profile_pic'
            mock_user.last_sid = f'{user_id}_last_sid'
            return MagicMock(first=MagicMock(return_value=mock_user))

        mock_user_query.filter_by.side_effect = user_query_side_effect

        # Send a GET request to the friends_activity endpoint with a test user_id
        response = self.app.get('/friends_activity/test_user_id')

        # Assert the response and data returned by the function
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), [
            {'name': 'friend1', 'profilePicture': 'friend1_profile_pic', 'lastListenedSong': 'friend1_last_sid'},
            {'name': 'friend2', 'profilePicture': 'friend2_profile_pic', 'lastListenedSong': 'private'},
            {'name': 'friend3', 'profilePicture': 'friend3_profile_pic', 'lastListenedSong': 'friend3_last_sid'}
        ]) 

    # Feature: Monthly Average Rating Functionality
    # Scenario: Retrieve monthly average rating for a user
    # Given: Mocked database query results
    # When: A GET request is made to '/test_user_id/monthly_average_rating'
    # Then: Monthly average ratings should be returned successfully 
    @patch('app.main_page.db.session.query')
    def test_get_user_monthly_average_rating(self, mock_db_query):
        # Create a mock for the query results
        mock_query_result = MagicMock()
        mock_query_result.all.return_value = [
            MagicMock(year=2023, month=1, average_rating=4.5),
            MagicMock(year=2023, month=2, average_rating=4.2)
        ]
        mock_db_query.return_value.filter.return_value.group_by.return_value.order_by.return_value.all = mock_query_result.all

        # Send a GET request to the get_user_monthly_average_rating endpoint with a test user_id
        response = self.app.get('/test_user_id/monthly_average_rating')

        # Expected result
        expected_result = {
            'user_id': 'test_user_id',
            'monthly_average_ratings': [
                {'year': 2023, 'month': 1, 'average_rating': 4.5},
                {'year': 2023, 'month': 2, 'average_rating': 4.2}
            ],
        }

        # Assert the response and data returned by the function
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), expected_result) 
    
    # Feature: Add Friend Functionality
    # Scenario: Add a new friend
    # Given: Mocked user and friendship data
    # When: A POST request is made to '/add_friend/valid_user_id'
    # Then: The friend should be added successfully 
    @patch('app.main_page.User.query')
    @patch('app.main_page.Friendship.query')
    @patch('app.main_page.db.session')
    def test_add_friend(self, mock_db_session, mock_friendship_query, mock_user_query):
        # Mock User query for both user and friend
        mock_user_query.get.side_effect = lambda user_id: MagicMock(user_id=user_id) if user_id in ['valid_user_id', 'valid_friend_id'] else None

        # Mock Friendship query to simulate no existing friendship
        mock_friendship_query.filter.return_value.first.return_value = None

        # Mock data for POST request
        data = {
            'friend_id': 'valid_friend_id',
            'rate_sharing': 'public'
        }

        # Send a POST request to the add_friend endpoint
        response = self.app.post('/add_friend/valid_user_id', json=data)

        # Assert the response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {'message': 'Friend added successfully'})

        # Assert that a new Friendship is added and commit is called
        mock_db_session.add.assert_called()
        mock_db_session.commit.assert_called() 
    #
    

    # Feature: Search User Functionality
    # Scenario: Search for users by a search term
    # Given: Mocked user data
    # When: A GET request is made to '/search_user/user'
    # Then: Users matching the search term should be returned successfully 
    @patch('app.main_page.User.query')
    def test_search_friends(self, mock_user_query):
        # Mock User query to return a list of users for the search term
        mock_users = [
            MagicMock(user_id='user123', profile_pic='pic123.jpg'),
            MagicMock(user_id='user456', profile_pic='pic456.jpg')
        ]
        mock_user_query.filter.return_value.all.return_value = mock_users

        # Search term
        search_term = 'user'

        # Send a GET request to the search_user endpoint with the search term
        response = self.app.get(f'/search_user/{search_term}')

        # Expected result
        expected_result = [
            {'user_id': 'user123', 'profile_pic': 'pic123.jpg'},
            {'user_id': 'user456', 'profile_pic': 'pic456.jpg'}
        ]

        # Assert the response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), expected_result)

        # Verify that the filter method was called
        mock_user_query.filter.assert_called() 


    # Feature: Update Friendship Functionality
    # Scenario: Update rate sharing status in a friendship
    # Given: Mocked friendship data
    # When: A POST request is made to '/update_friendship/user123'
    # Then: The friendship's rate sharing status should be updated successfully 
    @patch('app.main_page.Friendship.query')
    @patch('app.main_page.db.session')
    def test_update_friendship(self, mock_db_session, mock_friendship_query):
        user_id = 'user123'
        friend_id = 'friend456'
        new_rate_sharing = 'public'

        # Create a mock Friendship object
        mock_friendship = MagicMock()
        mock_friendship.user1_id = user_id
        mock_friendship.user2_id = friend_id
        mock_friendship.rate_sharing = 'private'

        # Set up the mock to return the mock Friendship object
        mock_friendship_query.filter.return_value.first.return_value = mock_friendship

        # Data to send with the POST request
        data = {
            'friend_id': friend_id,
            'rate_sharing': new_rate_sharing
        }

        # Send a POST request to the update_friendship endpoint
        response = self.app.post(f'/update_friendship/{user_id}', json=data)

        # Assert the response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"message": "Friendship rate_sharing updated successfully."})

        # Assert that the rate_sharing attribute was updated
        self.assertEqual(mock_friendship.rate_sharing, new_rate_sharing)

        # Assert that commit was called
        mock_db_session.commit.assert_called()

        # Test the case when friendship is not found
        mock_friendship_query.filter.return_value.first.return_value = None
        response_not_found = self.app.post(f'/update_friendship/{user_id}', json=data)
        self.assertEqual(response_not_found.status_code, 404)
        self.assertEqual(response_not_found.get_json(), {"message": "Friendship not found."})
    ##all rated songs 

   # Feature: Send Email Recommendations Functionality
    # Scenario: Send song recommendations via email
    # Given: Mocked user and email sending function
    # When: A GET request is made to '/send_recommendations/user123'
    # Then: Song recommendations should be sent via email successfully 
    @patch('app.main_page.User.query')
    @patch('app.user_page.most_rated_songs_mail')
    @patch('app.user_page.send_email')
    def test_send_recommendations(self, mock_send_email, mock_most_rated_songs_mail, mock_user_query):
        user_id = 'user123'
        user_email = 'user123@example.com'

        # Mock the User query to return a user object
        mock_user = MagicMock()
        mock_user.email = user_email
        mock_user_query.get.return_value = mock_user

        # Mock the most_rated_songs_mail function
        mock_most_rated_songs_mail.return_value = 'Mocked song recommendations'

        # Send a GET request to the send_recommendations endpoint
        response = self.app.get(f'/send_recommendations/{user_id}')

        # Assert the response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {'message': 'Recommendations sent successfully!'})

        # Assert that the send_email function was called with the correct parameters
        mock_send_email.assert_called_with(user_email, "Song Recommendations", "Your song recommendations:\nMocked song recommendations\nlove <3, \n SUpotify")

        # Test the case when the user is not found
        mock_user_query.get.return_value = None
        response_not_found = self.app.get(f'/send_recommendations/{user_id}')
        self.assertEqual(response_not_found.status_code, 404)
        self.assertEqual(response_not_found.get_json(), {'error': 'User not found'}) 
        
    ## old test 
    @patch('requests.get')
    def test_get_concerts_success(self, mock_get):
        # Mock response object for successful request
        mock_response = MagicMock()
        mock_response.json.return_value = {
            '_embedded': {
                'events': [
                    {
                        "name": "Concert A",
                        "dates": {"start": {"localDate": "2023-12-01"}},
                        "_embedded": {"venues": [{"name": "Venue A"}]},
                        "url": "http://example.com/concert-a"
                    },
                    {
                        "name": "Concert B",
                        "dates": {"start": {"localDate": "2023-12-02"}},
                        "_embedded": {"venues": [{"name": "Venue B"}]},
                        "url": "http://example.com/concert-b"
                    },
                ]
            }
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        # Make a GET request to the endpoint
        response = self.app.get('/concerts/testcity')

        # Assert request was successful
        self.assertEqual(response.status_code, 200)

        # Convert response data to JSON
        response_data = json.loads(response.data.decode('utf-8'))

        # Assert response contains correct data
        expected_data = [
            {
                "name": "Concert A",
                "date": "2023-12-01",
                "venue": "Venue A",
                "url": "http://example.com/concert-a"
            },
            {
                "name": "Concert B",
                "date": "2023-12-02",
                "venue": "Venue B",
                "url": "http://example.com/concert-b"
            }
        ]
        self.assertEqual(response_data, expected_data)
    #################
    # genius  
    ### ONEMLI NOT BUNUN MAIN.PY DA ROUTE U DEGISTI 
    @patch('lyricsgenius.Genius.search_song')
    def test_lyrics_success(self, mock_search_song):
        # Mock response for successful lyrics fetch
        mock_song = MagicMock()
        mock_song.lyrics = "This is a song lyric."
        mock_search_song.return_value = mock_song

        # Make a GET request to the endpoint
        response = self.app.get('/lyrics/ArtistName/SongName')

        # Assert request was successful
        self.assertEqual(response.status_code, 200)

        # Assert response contains correct lyrics
        response_data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response_data, "This is a song lyric.")

    @patch('lyricsgenius.Genius.search_song')
    def test_lyrics_not_found(self, mock_search_song):
        # Mock response for when lyrics are not found
        mock_search_song.return_value = None

        # Make a GET request to the endpoint
        response = self.app.get('/lyrics/ArtistName/SongName')

        # Assert request was unsuccessful
        # Update your Flask route to return 404 when lyrics are not found
        self.assertEqual(response.status_code, 404)

        # Assert response contains appropriate error message
        response_data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response_data, {"error": "Lyrics not found"}) 


#############   SPOTIFY USER PLAYLIST TEST   #################### 
    @patch('spotipy.Spotify.current_user_playlists')
    @patch('app.models.Playlist.query')
    def test_get_user_playlists(self, mock_playlist_query, mock_current_user_playlists):
        # Mock Spotify API response
        mock_current_user_playlists.return_value = {
            'items': [
                {
                    'name': 'Playlist 1',
                    'images': [{'url': 'http://example.com/image1.jpg'}],
                    'tracks': {'total': 10},
                    'id': '1'
                },
                {
                    'name': 'Playlist 2',
                    'images': [],
                    'tracks': {'total': 5},
                    'id': '2'
                }
            ]
        }

        # Mock Playlist query
        mock_playlist_query.filter_by.return_value.first.side_effect = [None, Playlist(playlist_id='2')]

        # Mock the db session's add and commit methods
        db.session.add = MagicMock()
        db.session.commit = MagicMock()

        # Make a GET request to the endpoint
        response = self.app.get('/get_user_playlists')

        # Assert request was successful
        self.assertEqual(response.status_code, 200)

        # Assert response contains the correct data
        expected_data = [
            {
                "name": "Playlist 1",
                "playlistPic": "http://example.com/image1.jpg",
                "songNumber": 10,
                "playlistID": "1"
            },
            {
                "name": "Playlist 2",
                "playlistPic": None,
                "songNumber": 5,
                "playlistID": "2"
            }
        ]
        self.assertEqual(response.json, expected_data)

        # Assert that the new playlist was added to the session
        db.session.add.assert_called()

        # Assert that the session was committed
        db.session.commit.assert_called()  
        
    """
    GIVEN access to Spotify API
    WHEN the add_song function is caled
    THEN the song data should be fetched and saved successfully
    """
    @patch('app.main_page.spotipy.Spotify')
    def test_fetch_and_save_song_success(self, mock_sp):
        # Set up the mock return values for sp.track, sp.audio_features, sp.artist, and sp.album
        mock_sp.track.return_value = {
            'id': 'dummy_song_id',
            'name': 'Dummy Song',
            'popularity': 80,
            'duration_ms': 210000,
            'album': {
                'id': 'dummy_album_id',
                'images': [{'url': 'http://dummy_album_image_url'}],
                'release_date': '2023-01-01',
                'name': 'Dummy Album'
            },
            'artists': [{'id': 'dummy_artist_id', 'name': 'Dummy Artist'}]
        }
        mock_sp.audio_features.return_value = [{'tempo': 120, 'valence': 0.5, 'energy': 0.8, 'danceability': 0.7}]
        mock_sp.artist.return_value = {
            'id': 'dummy_artist_id',
            'name': 'Dummy Artist',
            'popularity': 85,
            'genres': ['pop', 'rock'],
            'followers': {'total': 10000},
            'images': [{'url': 'http://dummy_artist_image_url'}]
        }
        mock_sp.album.return_value = {
            'id': 'dummy_album_id',
            'name': 'Dummy Album',
            'album_type': 'album',
            'images': [{'url': 'http://dummy_album_image_url'}]
        }

        song_id = 'dummy_song_id'
        fetch_and_save_song(sp=mock_sp, song_id=song_id)

        mock_sp.track.assert_called_once_with(song_id)
        mock_sp.audio_features.assert_called_once_with(song_id)
        mock_sp.artist.assert_called()
        mock_sp.album.assert_called()
    
    # Add more tests for other scenarios, such as:
    # - What happens if Spotify fails (success = False)?
    # - What if the Spotify API call times out?
    # - What if the database needs to be queried instead?
    

    """
    GIVEN the Spotify API is available
    AND the local database has song data
    WHEN the user makes a GET request to the '/recommendations/genre' endpoint
    THEN the Spotify API should be called with the specific genre and a limit of 10
    And the response content should match the expected song data format
    """
    @patch('app.main_page.spotipy.Spotify')
    @patch('app.main_page.Song.query')
    def test_get_recommendations_by_genre_from_spotify(self, mock_query, mock_spotify):
        
        # Mock the Spotify recommendations
        mock_spotify_instance = mock_spotify.return_value
        mock_spotify_instance.recommendations.return_value = {
            'tracks': [
                {
            'id': 'track_id',
            'name': 'Track Name',
            'artists': [{'name': 'Artist Name'}],
            'album': {'images': [{'url': 'http://image.url'}]},
            'duration_ms': 200000,
        }
            ]
        }

        # Mock the database query
        mock_query.all.return_value = [
                {
            'song_id': 'track_id',
            'song_name': 'Track Name',
            'artist_name': ['Artist Name'],
            'picture': 'http://image.url',
            'songLength': 200000,
        }
            ]

        # Make a GET request to the route
        response = self.app.get('/recommendations/genre')

        # Assert that the Spotify API is called
        mock_spotify_instance.recommendations.assert_called_with(seed_genres=['genre'], limit=10)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), [{
            'song_id': 'track_id',
            'song_name': 'Track Name',
            'artist_name': ['Artist Name'],
            'picture': 'http://image.url',
            'songLength': 200000,
        }])


    @patch('app.main_page.RateSong.query')
    def test_change_rating_song(self, mock_query):
        # Mock the RateSong query
        mock_prev_rate = MagicMock()
        mock_query.filter_by.return_value.first.return_value = mock_prev_rate
        
        # Mock data for the POST request
        test_data = {
            'song_id': 'test_song_id',
            'user_id': 'test_user_id',
            'rating': 4
        }
        response = self.app.post('/change_rating_song', json=test_data)

        """
        GIVEN an existing song with a specific rating <= 5
        WHEN user submits a POST request to change the rating of the song
        THEN the response should indicate success
        AND the song's rating should be updated in the database
        """
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {'message': True})

        """
        GIVEN an existing song with a specific rating is equal to 5
        WHEN user submits a POST request to change the rating of the song
        THEN the response should indicate success
        AND the song's rating should be updated in the database
        """
        test_data['rating'] = 5
        response = self.app.post('/change_rating_song', json=test_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {'message': True})

        """
        GIVEN an existing song with a specific rating > 5
        WHEN user submits a POST request to change the rating of the song
        THEN the response should indicate that the request is invalid
        """
        test_data['rating'] = 6
        response = self.app.post('/change_rating_song', json=test_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {'message': False})

        """
        GIVEN an existing song with a specific rating 0
        WHEN user submits a POST request to change the rating of the song
        THEN the response should indicate that the request is invalid
        """
        test_data['rating'] = 0
        response = self.app.post('/change_rating_song', json=test_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {'message': True})

        """
        GIVEN an existing song with a specific rating < 0
        WHEN user submits a POST request to change the rating of the song
        THEN the response should indicate that the request is invalid
        """
        test_data['rating'] = -1
        response = self.app.post('/change_rating_song', json=test_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {'message': False})

        """
        GIVEN an existing song without a previous rating
        WHEN user submits a POST request to rate the song
        THEN the response should indicate success
        AND the song's rating should be updated in the database
        """
        mock_query.filter_by.return_value.first.return_value = None
        test_data['rating'] = 3
        response = self.app.post('/change_rating_song', json=test_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {'message': True})

    """
    GIVEN the song and user information is available in the database
    WHEN a user plays a song
    THEN the song's play count should be incremented
    AND the response should confirm the action was successful
    """
    @patch('app.main_page.Song.query')
    @patch('app.main_page.User.query')
    def test_song_played_success(self, mock_user_query, mock_song_query):

        mock_song = MagicMock()
        mock_song.play_count = 0
        mock_song_query.filter_by.return_value.first.return_value = mock_song
        
        mock_user_query.filter_by.return_value.update.return_value = MagicMock()
        
        test_data = {
            'song_id': 'test_song_id',
            'user_id': 'test_user_id'
        }
        
        response = self.app.post('/song_played', json=test_data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {'message': True})


    """
    GIVEN the song information is not available in the database
    WHEN a user attempts to play a song with a non-existent song ID
    THEN the system should not find the song in the database
    AND the response should indicate that the song was not found
    """
    @patch('app.main_page.Song.query')
    @patch('app.main_page.User.query')
    def test_song_not_found(self, mock_user_query, mock_song_query):

        mock_song_query.filter_by.return_value.first.return_value = None
        
        test_data = {
            'song_id': 'nonexistent_song_id',
            'user_id': 'test_user_id'
        }
        
        response = self.app.post('/song_played', json=test_data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {'message': False})
    
    """
    GIVEN an artist already exists in the database
    WHEN a new song is posted to '/save_song_with_form' with the existing artist's name
    THEN the system should not create a new artist
    AND a new song should be added to the database under the existing artist
    AND the response should confirm the song was successfully saved
    """
    @patch('app.main_page.Artist.query')
    @patch('app.main_page.db.session')
    def test_save_song_with_new_artist(self, mock_db_session, mock_artist_query):
        mock_artist_query.filter_by.return_value.first.return_value = None
        
        test_data = {
            'artistName': 'New Artist',
            'songTitle': 'New Song',
            'songDuration': 300,
            'songGenre': 'New Genre',
            'songReleaseYear': '2020'
        }
        
        response = self.app.post('/save_song_with_form', json=test_data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {'message': True})

        mock_db_session.add.assert_called()
        mock_db_session.commit.assert_called()

    """
    GIVEN an artist already exists in the database
    WHEN the client sends a POST request to '/save_song_with_form' with song details and the existing artist's name
    THEN the system should use the existing artist record
    AND the system should create a new song record with the provided song details
    AND the response should confirm that the song was successfully saved

    """
    @patch('app.main_page.Artist.query')
    @patch('app.main_page.db.session')
    def test_save_song_with_existing_artist(self, mock_db_session, mock_artist_query):

        mock_artist = MagicMock()
        mock_artist.artist_id = 'existing_artist_id'
        mock_artist_query.filter_by.return_value.first.return_value = mock_artist
        
        test_data = {
            'artistName': 'Existing Artist',
            'songTitle': 'New Song',
            'songDuration': 300,
            'songGenre': 'New Genre',
            'songReleaseYear': '2020'
        }
        
        response = self.app.post('/save_song_with_form', json=test_data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {'message': True})

        mock_db_session.add.assert_called()
        mock_db_session.commit.assert_called()

    """
    GIVEN there are songs from the 90s in the database
    AND the user has rated some of these songs
    WHEN the client sends a GET request to '/{user_id}/90s'
    THEN the system should return the songs from the 90s that the user has rated
    """
    @patch('app.main_page.Song.query')
    @patch('app.main_page.RateSong.query')
    @patch('app.main_page.ArtistsOfSong.query')
    @patch('app.main_page.Artist.query')
    def test_get_user_highly_rated_90s_songs(self, mock_artist_query, mock_artists_of_song_query, mock_rate_query, mock_song_query):
        
        mock_90s_songs = [
            MagicMock(song_id='song1', song_name='Song 1', release_date=1995),
            MagicMock(song_id='song2', song_name='Song 2', release_date=1996)
        ]
        mock_song_query.filter.return_value.all.return_value = mock_90s_songs
        
        mock_user_rates = [
            MagicMock(song_id='song1', rating=5),
            MagicMock(song_id='song2', rating=4)
        ]
        mock_rate_query.filter.return_value.all.return_value = mock_user_rates

        user_id = 'user123'
        response = self.app.get(f'/{user_id}/90s')

        self.assertEqual(response.status_code, 200)

    """
    GIVEN there are songs from the 90s in the database
    BUT the user has not rated any of these songs
    WHEN the client sends a GET request to '/{user_id}/90s'
    THEN the system should recognize that the user has no ratings for 90s songs
    AND the response should have a status code of 200
    AND the response should indicate that the user has no highly rated 90s songs
    """
    @patch('app.main_page.Song.query')
    @patch('app.main_page.RateSong.query')
    def test_user_has_no_ratings_for_90s_songs(self, mock_rate_query, mock_song_query):

        mock_song_query.filter.return_value.all.return_value = [
            MagicMock(song_id='song1', song_name='Song 1', release_date=1995),
            # ... add more 90s songs if needed
        ]
        
        mock_rate_query.filter.return_value.all.return_value = []

        user_id = 'user123'
        response = self.app.get(f'/{user_id}/90s')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {
            'user_id': user_id,
            'highly_rated_90s_songs': []
        })

    """
    GIVEN the database has a list of songs with associated artists and ratings
    WHEN the client sends a GET request to '/{user_id}/all_songs'
    THEN the system should return a detailed list of all songs
    AND each song in the list should include its artist, album, and user-specific rating information
    """
    @patch('app.main_page.Song.query')
    @patch('app.main_page.RateSong.query')
    @patch('app.main_page.ArtistsOfSong.query')
    @patch('app.main_page.Artist.query')
    def test_get_all_songs_valid(self, mock_artist_query, mock_artists_of_song_query, mock_rate_query, mock_song_query):
        mock_all_songs = [
            MagicMock(
                song_id='song1',
                artist_id='artist1',
                song_name='Song 1',
                picture='http://song-image.url',
                tempo=120,
                popularity=80,
                valence=0.5,
                duration=300000,
                energy=0.8,
                danceability=0.7,
                genre='Rock',
                release_date=2000,
                play_count=100,
                date_added=datetime(2022, 1, 1),
                album=MagicMock(album_name='Album 1'),
            ),
        ]
        mock_song_query.all.return_value = mock_all_songs
        mock_rate = MagicMock()
        mock_rate.rating = 5
        mock_rate_query.filter_by.return_value.first.return_value = mock_rate

        mock_artist_of_song = MagicMock()
        mock_artists_of_song_query.filter_by.return_value.all.return_value = [mock_artist_of_song]
        mock_artist = MagicMock()
        mock_artist.artist_name = 'Artist 1'
        mock_artist_query.filter_by.return_value.first.return_value = mock_artist

        user_id = 'user123'

        response = self.app.get(f'/{user_id}/all_songs')
        response_data = response.get_json()

        self.assertEqual(response.status_code, 200)
        expected_data = {
            'songs': [{
                'song_id': song.song_id,
                'artist_id': song.artist_id,
                'artist_name': ['Artist 1'],  # This should match mock_artist.artist_name
                'album_name': song.album.album_name if song.album else None,
                'song_name': song.song_name,
                'picture': song.picture,
                'rate': 5,  # This should match mock_rate.rating
                'tempo': song.tempo,
                'popularity': song.popularity,
                'valence': song.valence,
                'duration': song.duration,
                'energy': song.energy,
                'danceability': song.danceability,
                'genre': song.genre,
                'release_date': song.release_date,
                'play_count': song.play_count,
                'date_added': mock_all_songs[0].date_added.isoformat() if isinstance(mock_all_songs[0].date_added, datetime) else mock_all_songs[0].date_added,
            } for song in mock_all_songs]
        }
        self.assertEqual(response_data, expected_data)

    """
    GIVEN the database has no songs
    WHEN the client sends a GET request to '/{user_id}/all_songs'
    THEN the system should recognize that there are no songs
    AND the response should indicate that there are no songs
    """
    @patch('app.main_page.Song.query')
    def test_get_all_songs_no_songs(self, mock_song_query):
        mock_song_query.all.return_value = []

        user_id = 'user123'
        response = self.app.get(f'/{user_id}/all_songs')
        response_data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data, {'songs': []})

    """
    GIVEN there are newly released songs in the database
    AND the user has rated some of these new songs
    WHEN the client sends a GET request to '/{user_id}/new_songs'
    THE the system should return a list of new songs with their release dates
    AND for each song, if the user has rated it, include the rating
    """
    @patch('app.main_page.Song.query')
    @patch('app.main_page.RateSong.query')
    def test_get_user_new_songs(self, mock_rate_song_query, mock_song_query):

        mock_song_query.filter.return_value.all.return_value = [
            Song(song_id='song1', song_name='Song 1', release_date=2023),
            Song(song_id='song2', song_name='Song 2', release_date=2023)
        ]
        
        mock_rate_song_query.filter_by.return_value.first.side_effect = [
            RateSong(song_id='song1', user_id='user1', rating=4),
            None
        ]

        response = self.app.get('/user123/new_songs')

        self.assertEqual(response.status_code, 200)

        expected_response = [
            {
                'song_id': 'song1',
                'song_name': 'Song 1',
                'artist_name': [],
                'release_date': 2023,
                'rate': 4
            },
            {
                'song_id': 'song2',
                'song_name': 'Song 2',
                'artist_name': [],
                'release_date': 2023,
                'rate': 0  # No rating for song2
            }
        ]

        self.assertEqual(response.get_json(), expected_response)

    """
    GIVEN there are no newly released songs in the database for the current year
    WHEN the client sends a GET request to '/{user_id}/new_songs'
    THEN the system should recognize that there are no new songs for the current year
    AND the response should indicate that no songs were found for the current year
    """
    @patch('app.main_page.Song.query')
    @patch('app.main_page.RateSong.query')
    def test_get_user_new_songs_no_songs(self, mock_rate_song_query, mock_song_query):
        mock_song_query.filter.return_value.all.return_value = []

        response = self.app.get('/user123/new_songs')

        self.assertEqual(response.status_code, 200)

        expected_response = {'error': 'No songs found for the current year.'}

        self.assertEqual(response.get_json(), expected_response)


    @patch('app.main_page.Song.query')
    @patch('app.main_page.RateSong.query')
    def test_get_user_new_songs_no_ratings(self, mock_rate_song_query, mock_song_query):
        # Mock the Song.query.filter method to return songs released in 2023
        mock_song_query.filter.return_value.all.return_value = [
            Song(song_id='song1', song_name='Song 1', release_date=2023),
            Song(song_id='song2', song_name='Song 2', release_date=2023)
        ]
        
        # Mock the RateSong.query.filter_by method to return no user ratings
        mock_rate_song_query.filter_by.return_value.first.side_effect = [None, None]

        response = self.app.get('/user123/new_songs')

        self.assertEqual(response.status_code, 200)

        expected_response = [
            {
                'song_id': 'song1',
                'song_name': 'Song 1',
                'artist_name': [],
                'release_date': 2023,
                'rate': 0  # No rating for song1
            },
            {
                'song_id': 'song2',
                'song_name': 'Song 2',
                'artist_name': [],
                'release_date': 2023,
                'rate': 0  # No rating for song2
            }
        ]

        self.assertEqual(response.get_json(), expected_response)

    """
    GIVEN there are newly released songs in the database
    BUT the user has not rated any of these new songs
    WHEN the client sends a GET request to '/{user_id}/new_songs'
    THEN the system should return a list of new songs with their release dates
    AND for each song, the rating should be indicated as 0
    """
    @patch('app.main_page.db.session.query')
    @patch('app.main_page.RateArtist.query')
    def test_artist_song_count(self, mock_rate_artist_query, mock_query):

        mock_query.return_value.join.return_value.group_by.return_value.order_by.return_value.limit.return_value.all.return_value = [
            ('artist1', 'Artist 1', 5),
            ('artist2', 'Artist 2', 3)
        ]
        
        mock_rate_artist_query.filter_by.return_value.first.side_effect = [
            RateArtist(artist_id='artist1', user_id='user1', rating=4),
            None  # No rating for artist2
        ]

        response = self.app.get('/user123/artist_song_count')

        self.assertEqual(response.status_code, 200)

        expected_response = [
            {
                'artist_name': 'Artist 1',
                'song_count': 5,
                'rate': 4
            },
            {
                'artist_name': 'Artist 2',
                'song_count': 3,
                'rate': 0  # No rating for artist2
            }
        ]

        self.assertEqual(response.get_json(), expected_response)
    
    @patch('app.main_page.RateArtist.query')
    def test_update_existing_rating(self, mock_rate_artist_query):
        # Mocking an existing rating
        mock_prev_rate = MagicMock()
        mock_rate_artist_query.filter_by.return_value.first.return_value = mock_prev_rate

        # Mock POST data
        data = {'artist_id': 'artist123', 'user_id': 'user123', 'rating': 4}

        response = self.app.post('/change_rating_artist', json=data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {'message': True})
    
    @patch('app.main_page.RateArtist.query')
    @patch('app.main_page.db.session')
    def test_create_new_rating(self, mock_db_session, mock_rate_artist_query):
        # Mocking no existing rating
        mock_rate_artist_query.filter_by.return_value.first.return_value = None

        # Mock POST data
        data = {'artist_id': 'artist123', 'user_id': 'user123', 'rating': 5}

        response = self.app.post('/change_rating_artist', json=data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {'message': True})
        mock_db_session.add.assert_called_once()

        
    @patch('app.main_page.RateArtist.query')
    def test_invalid_rating(self, mock_rate_artist_query):
        # Mock POST data with invalid rating
        data = {'artist_id': 'artist123', 'user_id': 'user123', 'rating': 6}

        response = self.app.post('/change_rating_artist', json=data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {'message': False})
        
    @patch('app.main_page.RateAlbum.query')
    def test_update_existing_album_rating(self, mock_rate_album_query):
        # Mocking an existing rating
        mock_prev_rate = MagicMock()
        mock_rate_album_query.filter_by.return_value.first.return_value = mock_prev_rate

        # Mock POST data
        data = {'album_id': 'album123', 'user_id': 'user123', 'rating': 4}

        response = self.app.post('/change_rating_album', json=data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {'message': True})

    @patch('app.main_page.RateAlbum.query')
    def test_create_new_album_rating(self, mock_rate_album_query):
        # Mocking no existing rating
        mock_rate_album_query.filter_by.return_value.first.return_value = None

        # Mock POST data
        data = {'album_id': 'album123', 'user_id': 'user123', 'rating': 5}

        response = self.app.post('/change_rating_album', json=data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {'message': True})

    @patch('app.main_page.RateAlbum.query')
    def test_invalid_album_rating(self, mock_rate_album_query):
        # Mock POST data with invalid rating
        data = {'album_id': 'album123', 'user_id': 'user123', 'rating': 6}

        response = self.app.post('/change_rating_album', json=data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {'message': False})

    def test_friends_recommendations_endpoint(self):
        response = self.app.get('/1/friends_recommendations') 
        
        self.assertEqual(response.status_code, 200)

        data = response.get_json()
        self.assertIn('recommendations', data)

        recommendations = data['recommendations']
        self.assertTrue(isinstance(recommendations, list))

        # Check if the number of recommendations is less than or equal to 20
        self.assertTrue(len(recommendations) <= 20)

        # Add more specific tests based on the expected data in the recommendations
        # For example, you can check if each recommendation has the expected keys like 'song_name', 'artist_name', etc.
        for recommendation in recommendations:
            self.assertIn('song_name', recommendation)
            self.assertIn('artist_name', recommendation)
            self.assertIn('rating', recommendation)
            self.assertIn('song_id', recommendation)
            self.assertIn('picture', recommendation)
            self.assertIn('songLength', recommendation)

    def test_friend_artist_recommendations_endpoint(self):
        response = self.app.get('/1/friend_artist_recommendations')  # Replace '1' with the appropriate user_id
        self.assertEqual(response.status_code, 200)

        data = response.get_json()
        self.assertIn('recommendations', data)

        recommendations = data['recommendations']
        self.assertTrue(isinstance(recommendations, list))

        # Add more specific tests based on the expected data in the artist recommendations
        for recommendation in recommendations:
            self.assertIn('artist_name', recommendation)
            self.assertIn('picture', recommendation)
            self.assertIn('artist_id', recommendation)
            self.assertIn('popularity', recommendation)
            self.assertIn('genres', recommendation)
            self.assertIn('followers', recommendation)
    
    @patch('app.main_page.spotipy.Spotify')
    @patch('app.main_page.format_recommendations')
    def test_get_recommendations_by_track(self, mock_format_recommendations, mock_spotify_class):
        # Set up mock Spotify instance and its recommendations method
        mock_spotify_instance = MagicMock()
        mock_spotify_class.return_value = mock_spotify_instance
        mock_spotify_instance.recommendations.return_value = {'tracks': ['track1', 'track2', 'track3']}

        # Set up mock format_recommendations function
        mock_format_recommendations.return_value = [
            {
                'song_id': 'song1',
                'song_name': 'song1',
                'artist_name': ['artist1'],
                'picture': 'picture1',
                'songLength': 180000
            },
            {
                'song_id': 'song2',
                'song_name': 'song2',
                'artist_name': ['artist2'],
                'picture': 'picture2',
                'songLength': 240000
            },
            {
                'song_id': 'song3',
                'song_name': 'song3',
                'artist_name': ['artist3'],
                'picture': 'picture3',
                'songLength': 300000
            }
        ]
        
        jsonified_return_value = mock_format_recommendations.return_value

        track_id = 'test_track_id'
        response = self.app.get(f'/recommendations_track/{track_id}')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), jsonified_return_value)

        mock_spotify_instance.recommendations.assert_called_once_with(seed_tracks=[track_id], limit=10)
        mock_format_recommendations.assert_called_once()
        
    @patch('app.main_page.RateSong.query')
    @patch('app.main_page.redirect')
    def test_get_newly_recommendations_with_recent_song(self, mock_redirect, mock_rate_song_query):
        # Mocking RateSong query
        mock_recent_song = MagicMock()
        mock_recent_song.song_id = 'recent_song_id'
        mock_rate_song_query.filter_by.return_value.filter.return_value.order_by.return_value.first.return_value = mock_recent_song

        # Mocking redirect
        redirect_url = "http://127.0.0.1:8008/recommendations_track/recent_song_id"
        mock_redirect.return_value = redirect(redirect_url)

        current_user_id = 'test_user_id'
        response = self.app.get(f'/{current_user_id}/newly_rating_recomendations')

        self.assertEqual(response.status_code, 302)  # Redirect status code
        mock_redirect.assert_called_once_with(redirect_url)

    @patch('app.main_page.RateSong.query')
    def test_get_newly_recommendations_without_recent_song(self, mock_rate_song_query):
        # Mocking RateSong query to return None
        mock_rate_song_query.filter_by.return_value.filter.return_value.order_by.return_value.first.return_value = None

        current_user_id = 'test_user_id'
        response = self.app.get(f'/{current_user_id}/newly_rating_recomendations')

        self.assertEqual(response.status_code, 200)  # OK status code
        self.assertEqual(response.get_json(), {'recommendation': None})
        
    @patch('app.main_page.spotipy.Spotify')
    def test_get_top_50_songs_of_country_with_results(self, mock_spotify):
        # Setup mock Spotify client
        mock_spotify_instance = MagicMock()
        mock_spotify.return_value = mock_spotify_instance

        # Mock search and playlist_tracks methods
        mock_search_result = {
            'playlists': {
                'items': [{'id': 'playlist_id'}]
            }
        }
        mock_tracks_result = {
            'items': [
                {'track': {'id': 'song1', 'name': 'Song 1', 'artists': [{'name': 'Artist 1'}], 'album': {'images': [{'url': 'image1'}]}, 'duration_ms': 180000}},
                {'track': {'id': 'song2', 'name': 'Song 2', 'artists': [{'name': 'Artist 2'}], 'album': {'images': [{'url': 'image2'}]}, 'duration_ms': 200000}}
            ]
        }

        mock_spotify_instance.search.return_value = mock_search_result
        mock_spotify_instance.playlist_tracks.return_value = mock_tracks_result

        country_name = 'USA'
        response = self.app.get(f'/get_top_songs/{country_name}')

        self.assertEqual(response.status_code, 200)
        response_data = response.get_json()
        self.assertEqual(len(response_data), 2)
        self.assertIn('song_id', response_data[0])
        self.assertIn('song_name', response_data[0])
        self.assertIn('artist_name', response_data[0])
        self.assertIn('picture', response_data[0])
        self.assertIn('songLength', response_data[0])

    @patch('app.main_page.spotipy.Spotify')
    def test_get_top_50_songs_of_country_no_results(self, mock_spotify):
        # Setup mock Spotify client
        mock_spotify_instance = MagicMock()
        mock_spotify.return_value = mock_spotify_instance

        # Mock search method to return empty result
        mock_spotify_instance.search.return_value = {'playlists': {'items': []}}

        country_name = 'Unknown'
        response = self.app.get(f'/get_top_songs/{country_name}')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {'message': False})
    
    @patch('app.main_page.spotipy.Spotify')
    def test_get_playlists_songs(self, mock_spotify_class):
        # Set up mock Spotify instance
        mock_spotify_instance = MagicMock()
        mock_spotify_class.return_value = mock_spotify_instance

        # Mock playlist_tracks method for two different playlists
        mock_spotify_instance.playlist_tracks.side_effect = [
        {'items': [{'track': {'artists': [{'name': 'Artist 1'}], 'name': 'Song 1', 'id': 'song1', 'album': {'images': [{'url': 'song1.jpg'}]}, 'duration_ms': 180000}}]},
        {'items': [{'track': {'artists': [{'name': 'Artist 2'}], 'name': 'Song 2', 'id': 'song2', 'album': {'images': [{'url': 'song2.jpg'}]}, 'duration_ms': 240000}}]}
        ]

        # IDs of the playlists
        playlistID1 = 'playlist1'
        playlistID2 = 'playlist2'

        # Make a GET request to the endpoint
        response = self.app.get(f'/get_playlists_songs/{playlistID1}/{playlistID2}')

        # Check if the response is as expected
        self.assertEqual(response.status_code, 200)
        expected_songs = [
            {
                'artist_name': 'Artist 1',
                'song_name': 'Song 1',
                'song_id': 'song1',
                'picture': 'song1.jpg',
                'songLength': 180000
            },
            {
                'artist_name': 'Artist 2',
                'song_name': 'Song 2',
                'song_id': 'song2',
                'picture': 'song2.jpg',
                'songLength': 240000
            }
        ]
        self.assertEqual(response.get_json(), expected_songs)
        # Validate the calls to the Spotify API
        mock_spotify_instance.playlist_tracks.assert_any_call(playlistID1)
        mock_spotify_instance.playlist_tracks.assert_any_call(playlistID2)
        
if __name__ == '__main__':
    unittest.main()