from flask import Flask
import unittest
from flask_sqlalchemy import SQLAlchemy
from app import create_app, db
import json
from unittest.mock import patch, MagicMock
from app.main_page import fetch_and_save_song 
from datetime import datetime
import time
import threading

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

    def test_song_played_performance(self):
        num_requests = 1000 
        song_id = 'song_id'
        user_id = 'user_id'
        data = {'song_id': song_id, 'user_id': user_id}
        concurrency = 50  # Number of concurrent requests
        def make_request():
            response = self.app.post('/song_played', json=data)
            self.assertEqual(response.status_code, 200)

        start_time = time.time()

        threads = []
        for _ in range(concurrency):
            thread = threading.Thread(target=make_request)
            threads.append(thread)

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        end_time = time.time()
        elapsed_time = end_time - start_time

        requests_per_second = num_requests / elapsed_time

        max_response_time = 2
        self.assertLess(elapsed_time, max_response_time)


    def test_change_rating_song_performance_large_requests(self):
        song_id = "your_song_id"  # Replace with an actual song_id
        user_id = "your_user_id"  # Replace with an actual user_id
        rating = 4  # Rating to set for the song
        num_requests = 100  # Number of requests to send
        
        total_execution_time = 0
        
        for _ in range(num_requests):
            # Measure the time before calling the function
            start_time = time.time()
            
            # Create JSON data for the POST request
            data = {
                'song_id': song_id,
                'user_id': user_id,
                'rating': rating
            }
            
            # Call the change_rating_song function with a POST request
            response = self.app.post('/change_rating_song', json=data)
            
            # Measure the time after calling the function
            end_time = time.time()
            
            # Calculate the execution time for each request
            execution_time = end_time - start_time
            total_execution_time += execution_time
        
            # Assert that the response status code is 200
            self.assertEqual(response.status_code, 200)
        
        average_execution_time = total_execution_time / num_requests

        max_allowed_time = 3.0
        print(f"Average execution time for change_rating_song ({num_requests} requests): {average_execution_time} seconds")
        self.assertLess(total_execution_time, max_allowed_time)

    
    def test_song_large_requests(self):
        song_id = "11dFghVXANMlKmJXsNCbNl"  
        user_id = "1"  
        num_requests = 100 
        
        total_execution_time = 0
        
        for _ in range(num_requests):
            start_time = time.time()
            
            data = {
                'song_id': song_id,
                'user_id': user_id
            }
            
            response = self.app.post('/song_played', json=data)
            
            end_time = time.time()
            
            execution_time = end_time - start_time
            total_execution_time += execution_time
        
            self.assertEqual(response.status_code, 200)
        
        average_execution_time = total_execution_time / num_requests
        max_allowed_time = 3.0
        self.assertLess(total_execution_time, max_allowed_time)

    def test_save_song_with_form_performance_large_requests(self):
        num_requests = 1
        
        total_execution_time = 0
        
        for i in range(num_requests):
            start_time = time.time()
            
            data = {
                'artistName': 'Artist Name',
                'songTitle': f'Song Title{i}',
                'songDuration': 200000,
                'songGenre': 'Genre',
                'songReleaseYear': '2023'
            }
            
            response = self.app.post('/save_song_with_form', json=data)
            
            end_time = time.time()
            
            execution_time = end_time - start_time
            total_execution_time += execution_time
        
            self.assertEqual(response.status_code, 200)
        
        max_allowed_time = 1.0
        average_execution_time = total_execution_time / num_requests
        self.assertLess(total_execution_time, max_allowed_time)
        print(f"Average execution time for save_song_with_form ({num_requests} requests): {average_execution_time} seconds")

    
    def test_artist_song_count_large_requests(self):
        user_id = "1"  
        num_requests = 100 
        total_execution_time = 0
        
        for _ in range(num_requests):
            start_time = time.time()
            
            # Send a GET request to the artist_song_count route
            response = self.app.get(f'/{user_id}/artist_song_count')
            
            end_time = time.time()
            
            execution_time = end_time - start_time
            total_execution_time += execution_time
            
            # Assert the response status code is 200
            self.assertEqual(response.status_code, 200)
        
        average_execution_time = total_execution_time / num_requests
        max_allowed_time = 1.0
        
        print(f"Average execution time per request: {average_execution_time} seconds.")
        
        self.assertLess(total_execution_time, max_allowed_time)



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