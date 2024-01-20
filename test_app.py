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
    

if __name__ == '__main__':
    unittest.main()