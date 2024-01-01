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
    


"""    @patch('app.models.User.query')
    @patch('app.models.Friendship.query')
    def test_user_page(self, mock_user_query, mock_friendship_query):
        # Given a mocked User and Friendship query
        user_instance = MagicMock()
        friend_instance1 = MagicMock()
        friend_instance2 = MagicMock()

        # Configure the mock instances as needed
        user_instance.first.return_value = User(
            user_id='testuser',
            profile_pic='test_profile_pic',
            last_sid='last_song_id'
        )

        friend_instance1.all.return_value = [
            Friendship(user1_id='testuser', user2_id='friend1'),
            Friendship(user1_id='testuser', user2_id='friend2')
        ]

        friend_instance2.all.return_value = [
            Friendship(user1_id='friend3', user2_id='testuser'),
            Friendship(user1_id='friend4', user2_id='testuser')
        ]

        mock_user_query.filter_by.return_value = user_instance
        mock_friendship_query.filter_by.side_effect = [friend_instance1, friend_instance2]

        # When a GET request is made to the user_page endpoint
        response = self.app.get('/user_data/test@example.com')

        # Then the response status code should be 200 (OK)
        self.assertEqual(response.status_code, 200)

        # And the response JSON should include the expected user information
        expected_response = {
            'username': 'testuser',
            'profilePicture': 'test_profile_pic',
            'lastListenedSong': 'last_song_id',
            'friends': ['friend1', 'friend2', 'friend3', 'friend4'],
            'friendsCount': 4
        }
        self.assertEqual(json.loads(response.data), expected_response)"""
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
 





if __name__ == '__main__':
    unittest.main()
