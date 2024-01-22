from flask import Flask
import unittest
from flask_sqlalchemy import SQLAlchemy
from app import create_app, db
import json
from unittest.mock import patch, MagicMock

from app.models import Album, Friendship, RateSong, SongPlaylist, Playlist, Artist, Song, User, RateArtist, RateAlbum, ArtistsOfSong

class BluePrintTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app().test_client()
        self.app_context = create_app().app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


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
                'user_id': 'testuser',
                'password': 'testpassword',
                'email': 'test@example.com'
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
if __name__ == '_main_':
    unittest.main()  


if __name__ == '__main__':
    unittest.main()
