from flask import Flask, redirect
import unittest
from flask_sqlalchemy import SQLAlchemy
from app import create_app, db
import json
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
    """
    # DOES NOT WORK
    @patch('app.main_page.find_most_liked_artist')
    @patch('app.main_page.Artist.query')
    @patch('app.main_page.spotipy.Spotify')
    def test_recommended_artist_songs_endpoint(self, mock_spotipy, mock_artist_query, mock_find_most_liked_artist):
        # Mock the Spotify API response
        mock_find_most_liked_artist.return_value = '1'
        mock_artist_query.filter_by.return_value.first.return_value = Artist(artist_name='Artist 1', artist_id='1')

        mock_spotify_instance = MagicMock()
        mock_spotipy.return_value = mock_spotify_instance
        mock_spotify_instance.artist_top_tracks.return_value = {
            'tracks': [
                {
                    'artists': [{'name': 'Artist 1'}],
                    'name': 'Song 1',
                    'id': 'song1',
                    'album': {'images': [{'url': 'song1.jpg'}], 'name': 'Album 1'},
                    'duration_ms': 180000
                },
                {
                    'artists': [{'name': 'Artist 1'}],
                    'name': 'Song 2',
                    'id': 'song2',
                    'album': {'images': [{'url': 'song2.jpg'}], 'name': 'Album 2'},
                    'duration_ms': 240000
                }
            ]
        }

        response = self.app.get('/recommended_artist_songs/1')

        self.assertEqual(response.status_code, 200)

        data = response.get_json()
        self.assertIn('song_recommendations', data)

        song_recommendations = data['song_recommendations']
        self.assertTrue(isinstance(song_recommendations, list))
        self.assertEqual(len(song_recommendations), 2)  # Assert that two songs are returned

        expected_songs = [
            {'artist_name': 'Artist 1', 'song_name': 'Song 1', 'song_id': 'song1', 'picture': 'song1.jpg', 'songLength': 180000},
            {'artist_name': 'Artist 1', 'song_name': 'Song 2', 'song_id': 'song2', 'picture': 'song2.jpg', 'songLength': 240000}
        ]
        self.assertEqual(song_recommendations, expected_songs)
        """
    
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
    
    """
    @patch('app.main_page.Artist.query')
    @patch('app.main_page.ArtistsOfSong.query')
    @patch('app.main_page.RateSong.query')
    @patch('app.main_page.Song.query')
    def test_enrich_rec(self, mock_song_query, mock_rate_song_query, mock_artists_of_song_query, mock_artist_query):
        # Mock Song query
        mock_songs = [
            MockSong('song1', 'Song 1', 'image1.jpg', 180000, '2022-01-01', 'Rock'),
            MockSong('song2', 'Song 2', 'image2.jpg', 200000, '2023-01-01', 'Rock')
        ]
        mock_song_query.filter.return_value.all.return_value = mock_songs

        # Mock ArtistsOfSong query
        mock_artists_of_song_query.filter_by.return_value.all.return_value = [MagicMock(artist_id='artist1')]

        # Mock Artist query
        mock_artist_query.filter_by.side_effect = lambda artist_id: MagicMock(artist_name='Artist 1') if artist_id == 'artist1' else MagicMock(artist_name='Artist 2')

        # Mock RateSong query
        mock_rate_song_query.filter_by.side_effect = lambda song_id, user_id: MagicMock(rating=4) if song_id == 'song1' else MagicMock(rating=3)

        user_id = 'user123'
        genre = 'Rock'
        response = self.app.get(f'/enrich_rec/{user_id}/{genre}')

        self.assertEqual(response.status_code, 200)
        response_data = response.get_json()
        self.assertTrue(isinstance(response_data, list))

        # Check the contents of the response
        self.assertEqual(len(response_data), 2)
        for song in response_data:
            self.assertIn('song_id', song)
            self.assertIn('song_name', song)
            self.assertIn('artist_name', song)
            self.assertIn('picture', song)
            self.assertIn('songLength', song)
            self.assertIn('release_date', song)
            self.assertIn('rate', song)
    """
        
if __name__ == '__main__':
    unittest.main()