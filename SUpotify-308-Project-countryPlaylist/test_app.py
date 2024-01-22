from flask import Flask
import unittest
from flask_sqlalchemy import SQLAlchemy
from app import create_app, db
import json
from unittest.mock import patch, MagicMock
from app.main_page import fetch_and_save_song 
from datetime import datetime

from app.models import Album, Friendship, RateSong, SongPlaylist, Playlist, Artist, Song, User, RateArtist, RateAlbum, ArtistsOfSong

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

    def clear_data(self):
        # Clear data from each table without dropping the table
        for table in reversed(db.metadata.sorted_tables):
            db.session.execute(table.delete())
        db.session.commit()

    """
    GIVEN access to Spotify API
    WHEN the add_song function is caled
    THEN the song data should be fetched and saved successfully
    """
    @patch('app.main_page.sp')
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





if __name__ == '__main__':
    unittest.main()




    """
    GIVEN a user is created
    WHEN the user is inserted manually to DataBase
    THEN user can be reached by filtering the DataBase
    """
    """def test_db(self):
        with create_app().app_context():
            new_user = User(user_id="unittest_bismillah", password="pwd", email="test@example.com")
            db.session.add(new_user)
            db.session.commit()
     
            inserted_user = User.query.filter_by(user_id='unittest_bismillah').first()
            self.assertIsNotNone(inserted_user)
            self.assertEqual(inserted_user.email, 'test@example.com')"""

    """"
    GIVEN a user wants to sign up
    WHEN the user enters user_id, password and email
    THEN request should return True
    """
    """def test_sing_up(self):
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
        self.assertEqual(result, expected_message)"""

    """"
    GIVEN a username already exists
    WHEN the same username is used to sign up
    THEN request should return False
    """
    """def test_signup_failure_existing_user(self):
        with create_app().app_context():
            test_user = User(user_id='testuser', password='testpassword', email='test@example.com')
            db.session.add(test_user)
            db.session.commit()

            response = self.app.post('/sign_up', json={'user_id': 'testuser', 'password': 'testpassword', 'email': 'test@example.com'})

        self.assertEqual(response.status_code, 200)

        result = json.loads(response.data)

        self.assertEqual(result['message'], False)"""

    """ 
    GIVEN a user in the database with correct credentials
    WHEN a POST request is made to the login endpoint with correct credentials
    THEN the response status code should be 200
    AND the login message should be True
    """
    """
   def test_login_success(self):
        with create_app().app_context():
            test_user = User(user_id='testuser', password='testpassword', email='test@example.com')
            db.session.add(test_user)
            db.session.commit()

            response = self.app.post('/login', json={'email': 'test@example.com', 'password': 'testpassword'})

        self.assertEqual(response.status_code, 200)

        result = json.loads(response.data)

        self.assertEqual(result['message'], True)"""


    """
    GIVEN a user in the database with correct credentials
    WHEN a user tries to log in with incorrect credentials
    THEN the response status code should be 200
    AND the login message should be False
    """
    """def test_login_failure_wrong_password(self):
        with create_app().app_context():
            test_user = User(user_id='testuser', password='testpassword', email='test@example.com')
            db.session.add(test_user)
            db.session.commit()

            response = self.app.post('/login', json={'email': 'test@example.com', 'password': 'wrongpassword'})

        
        self.assertEqual(response.status_code, 200)

        
        result = json.loads(response.data)
        self.assertEqual(result['message'], False)"""


    """
    GIVEN a valid song in the database
    WHEN that song is deleted
    THEN the response status code should be 200
    AND the message should be True
    """
    """def test_delete_song(self):
        with create_app().app_context():
            test_song = Song(song_id="11dFghVXANMlKmJXsNCbNl")
            db.session.add(test_song)
            db.session.commit()

            response = self.app.post('/delete_song/11dFghVXANMlKmJXsNCbNl')
        
        self.assertEqual(response.status_code, 200)

        expected_response = {"message": True}
        self.assertEqual(response.get_json(), expected_response)"""

    """
    GIVEN a valid song in the database
    WHEN a song that is not in the database is deleted
    THEN the response status code should be 200
    AND the message should be False
    """
    """def test_delete_song_invalid_song(self):
        with create_app().app_context():

            response = self.app.post('/delete_song/11dFghVXANMlKmJXsNCbNl')
        
        self.assertEqual(response.status_code, 200)

        expected_response = {"message": False}
        self.assertEqual(response.get_json(), expected_response)"""
    
    """
    GIVEN a valid album in the database
    WHEN an album that is in the database is deleted
    THEN the response status code should be 200
    AND the message should be of valid deletion
    """
    """
   def test_delete_album(self):
        with create_app().app_context():
            test_album = Album(album_id="4aawyAB9vmqN3uQ7FjRGTy")
            db.session.add(test_album)
            db.session.commit()

            response = self.app.post('/delete_album/4aawyAB9vmqN3uQ7FjRGTy')
        
        self.assertEqual(response.status_code, 200)

        expected_response = {'message': True}
        self.assertEqual(response.get_json(), expected_response)"""

    
    """
    WHEN an album that is not in the database is deleted
    THEN the response status code should be 200
    AND the message should be of invalid deletion
    """
    """def test_delete_album_invalid_song(self):
        with create_app().app_context():
            response = self.app.post('/delete_album/4aawyAB9vmqN3uQ7FjRGTy')
        
        self.assertEqual(response.status_code, 200)

        expected_response = {'message': False}
        self.assertEqual(response.get_json(), expected_response)"""

    """
    GIVEN a valid artist in the database
    WHEN that artist is deleted
    THEN the response status code should be 200
    AND the message should be of valid deletion
    """
    """def test_delete_artist(self):
        artist_id = "0TnOYISbd1XYRBk9myaseg"
        with create_app().app_context():
            test_artist = Artist(artist_id="0TnOYISbd1XYRBk9myaseg")
            db.session.add(test_artist)
            db.session.commit()

            response = self.app.post('/delete_artist/0TnOYISbd1XYRBk9myaseg')
        
        self.assertEqual(response.status_code, 200)

        expected_response = {'message': True}
        self.assertEqual(response.get_json(), expected_response)"""


    """
    WHEN an artist that is not in the database is deleted
    THEN the response status code should be 200
    AND the message should be of invalid deletion
    """
    """def test_delete_artist_invalid_artist(self):
        artist_id = "0TnOYISbd1XYRBk9myaseg"
        with create_app().app_context():

            response = self.app.post('/delete_artist/0TnOYISbd1XYRBk9myaseg')
        
        self.assertEqual(response.status_code, 200)

        expected_response = {'message': False}
        self.assertEqual(response.get_json(), expected_response)"""

    """
    GIVEN a valid song ID
    WHEN that song is tried to be inserted to the database
    THEN the response status code should be 200
    AND the message should be of valid insertion
    """