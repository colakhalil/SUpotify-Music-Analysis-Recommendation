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

    def test_update_friendship_performance(self):
        # Create 1000 users
        for i in range(1000):
            self.app.post('/users', json={'user_id': f'user{i}', 'username': f'username{i}', 'password': f'password{i}'})
        # Create 1000 friendships
        for i in range(1000):
            self.app.post('/friendships', json={'user1_id': f'user{i}', 'user2_id': f'user{i+1}', 'rate_sharing': 'private'})
        # Update 1000 friendships
        start = time.time()
        for i in range(1000):
            self.app.put('/friendships', json={'user1_id': f'user{i}', 'user2_id': f'user{i+1}', 'rate_sharing': 'public'})
        end = time.time()
        print(f'Time taken to update 1000 friendships: {end-start} seconds')
        # Delete 1000 friendships
        for i in range(1000):
            self.app.delete('/friendships', json={'user1_id': f'user{i}', 'user2_id': f'user{i+1}'})
        # Delete 1000 users
        for i in range(1000):
            self.app.delete('/users', json={'user_id': f'user{i}'}) 
    
    def test_user_data_performance(self):
        # Create a test user
        test_email = "test_user@example.com"
        self.app.post('/create_user', json={'email': test_email, 'password': 'password', 'username': 'test_user'}) 

        # Measure performance
        start_time = time.time()
        response = self.app.get(f'/user_data/{test_email}')
        end_time = time.time()

        # Ensure the request was successful
        self.assertEqual(response.status_code, 200)

        # Print the time taken
        print(f"Time taken to fetch user data: {end_time - start_time} seconds")

        # Delete the test user
        self.app.delete('/delete_user', json={'email': test_email})  
    
    def  test_friends_activity_performance (self):
        # Create 1000 users
        for i in range(1000):
            self.app.post('/users', json={'user_id': f'user{i}', 'username': f'username{i}', 'password': f'password{i}'})
        # Create 1000 friendships
        for i in range(1000):
            self.app.post('/friendships', json={'user1_id': f'user{i}', 'user2_id': f'user{i+1}', 'rate_sharing': 'private'})
        # Create 1000 rated songs
        for i in range(1000):
            self.app.post('/rate_songs', json={'user_id': f'user{i}', 'song_id': f'song{i}', 'rating': 5})
        # Get 1000 friends activities
        start = time.time()
        for i in range(1000):
            self.app.get('/friends_activity', json={'user_id': f'user{i}'})
        end = time.time()
        print(f'Time taken to get 1000 friends activities: {end-start} seconds')
        # Delete 1000 rated songs
        for i in range(1000):
            self.app.delete('/rate_songs', json={'user_id': f'user{i}', 'song_id': f'song{i}'})
        # Delete 1000 friendships
        for i in range(1000):
            self.app.delete('/friendships', json={'user1_id': f'user{i}', 'user2_id': f'user{i+1}'})
        # Delete 1000 users
        for i in range(1000):
            self.app.delete('/users', json={'user_id': f'user{i}'}) 
        
    def test_monthly_average_rating_performance (self):
        # Create 1000 users
        for i in range(1000):
            self.app.post('/users', json={'user_id': f'user{i}', 'username': f'username{i}', 'password': f'password{i}'})
        # Create 1000 rated songs
        for i in range(1000):
            self.app.post('/rate_songs', json={'user_id': f'user{i}', 'song_id': f'song{i}', 'rating': 5})
        # Get 1000 monthly average ratings
        start = time.time()
        for i in range(1000):
            self.app.get('/monthly_average_rating', json={'user_id': f'user{i}'})
        end = time.time()
        print(f'Time taken to get 1000 monthly average ratings: {end-start} seconds')
        # Delete 1000 rated songs
        for i in range(1000):
            self.app.delete('/rate_songs', json={'user_id': f'user{i}', 'song_id': f'song{i}'})
        # Delete 1000 users
        for i in range(1000):
            self.app.delete('/users', json={'user_id': f'user{i}'})
    
    def test_add_friends_performance (self):
        # Create 1000 users
        for i in range(1000):
            self.app.post('/users', json={'user_id': f'user{i}', 'username': f'username{i}', 'password': f'password{i}'})
        # Create 1000 friendships
        start = time.time()
        for i in range(1000):
            self.app.post('/friendships', json={'user1_id': f'user{i}', 'user2_id': f'user{i+1}', 'rate_sharing': 'private'})
        end = time.time()
        print(f'Time taken to create 1000 friendships: {end-start} seconds')
        # Delete 1000 friendships
        for i in range(1000):
            self.app.delete('/friendships', json={'user1_id': f'user{i}', 'user2_id': f'user{i+1}'})
        # Delete 1000 users
        for i in range(1000):
            self.app.delete('/users', json={'user_id': f'user{i}'})
        
    def test_search_friend_performance (self):
        # Create 1000 users
        for i in range(1000):
            self.app.post('/users', json={'user_id': f'user{i}', 'username': f'username{i}', 'password': f'password{i}'})
        # Get 1000 users
        start = time.time()
        for i in range(1000):
            self.app.get('/users', json={'user_id': f'user{i}'})
        end = time.time()
        print(f'Time taken to get 1000 users: {end-start} seconds')
        # Delete 1000 users
        for i in range(1000):
            self.app.delete('/users', json={'user_id': f'user{i}'}) 

    def test_most_rated_songs_performance (self):
        # Create 1000 rated songs
        for i in range(1000):
            self.app.post('/rate_songs', json={'user_id': f'user{i}', 'song_id': f'song{i}', 'rating': 5})
        # Get 1000 most rated songs
        start = time.time()
        self.app.get('/most_rated_songs')
        end = time.time()
        print(f'Time taken to get 1000 most rated songs: {end-start} seconds')
        # Delete 1000 rated songs
        for i in range(1000):
            self.app.delete('/rate_songs', json={'user_id': f'user{i}', 'song_id': f'song{i}'}) 

    def  test_all_rated_songs_performance (self):
        # Create 1000 rated songs
        for i in range(1000):
            self.app.post('/rate_songs', json={'user_id': f'user{i}', 'song_id': f'song{i}', 'rating': 5})
        # Get all rated songs
        start = time.time()
        self.app.get('/rate_songs')
        end = time.time()
        print(f'Time taken to get all rated songs: {end-start} seconds')
        # Delete 1000 rated songs
        for i in range(1000):
            self.app.delete('/rate_songs', json={'user_id': f'user{i}', 'song_id': f'song{i}'})

    def test_all_songs_performance (self):
        # Create 1000 songs
        for i in range(1000):
            self.app.post('/songs', json={'song_id': f'song{i}', 'title': f'title{i}', 'duration': 200000, 'genre': 'genre', 'release_year': '2023'})
        # Get all songs
        start = time.time()
        self.app.get('/songs')
        end = time.time()
        print(f'Time taken to get all songs: {end-start} seconds')
        # Delete 1000 songs
        for i in range(1000):
            self.app.delete('/songs', json={'song_id': f'song{i}'})
            
    def test_all_artists_performance (self):
        # Create 1000 artists
        for i in range(1000):
            self.app.post('/artists', json={'artist_id': f'artist{i}', 'name': f'name{i}'})
        # Get all artists
        start = time.time()
        self.app.get('/artists')
        end = time.time()
        print(f'Time taken to get all artists: {end-start} seconds')
        # Delete 1000 artists
        for i in range(1000):
            self.app.delete('/artists', json={'artist_id': f'artist{i}'})
    
    def test_all_albums_performance (self):
        # Create 1000 albums
        for i in range(1000):
            self.app.post('/albums', json={'album_id': f'album{i}', 'name': f'name{i}', 'release_year': '2023'})
        # Get all albums
        start = time.time()
        self.app.get('/albums')
        end = time.time()
        print(f'Time taken to get all albums: {end-start} seconds')
        # Delete 1000 albums
        for i in range(1000):
            self.app.delete('/albums', json={'album_id': f'album{i}'})
    
    def test_get_song_info_performance(self):
        # Create 1000 songs
        for i in range(1000):
            self.app.post('/songs', json={'song_id': f'song{i}', 'title': f'title{i}', 'duration': 200000, 'genre': 'genre', 'release_year': '2023'})
        # Get 1000 songs
        start = time.time()
        for i in range(1000):
            self.app.get(f'/songs/{i}')
        end = time.time()
        print(f'Time taken to get 1000 songs: {end-start} seconds')
        # Delete 1000 songs
        for i in range(1000):
            self.app.delete('/songs', json={'song_id': f'song{i}'})
            
    def test_new_songs_performance(self):
        # Create 1000 songs
        for i in range(1000):
            self.app.post('/songs', json={'song_id': f'song{i}', 'title': f'title{i}', 'duration': 200000, 'genre': 'genre', 'release_year': '2023'})
        # Get 1000 new songs
        start = time.time()
        for i in range(1000):
            self.app.get('/new_songs')
        end = time.time()
        print(f'Time taken to get 1000 new songs: {end-start} seconds')
        # Delete 1000 songs
        for i in range(1000):
            self.app.delete('/songs', json={'song_id': f'song{i}'})
    
    def test_change_rating_artist_performance(self):
        # Create 1000 artists
        for i in range(1000):
            self.app.post('/artists', json={'artist_id': f'artist{i}', 'name': f'name{i}'})
        # Create 1000 rated artists
        for i in range(1000):
            self.app.post('/rate_artists', json={'user_id': f'user{i}', 'artist_id': f'artist{i}', 'rating': 5})
        # Update 1000 rated artists
        start = time.time()
        for i in range(1000):
            self.app.put('/rate_artists', json={'user_id': f'user{i}', 'artist_id': f'artist{i}', 'rating': 1})
        end = time.time()
        print(f'Time taken to update 1000 rated artists: {end-start} seconds')
        # Delete 1000 rated artists
        for i in range(1000):
            self.app.delete('/rate_artists', json={'user_id': f'user{i}', 'artist_id': f'artist{i}'})
        # Delete 1000 artists
        for i in range(1000):
            self.app.delete('/artists', json={'artist_id': f'artist{i}'})
            
            
    def test_friends_recommendation_performance(self):
        # Create 1000 users
        for i in range(1000):
            self.app.post('/users', json={'user_id': f'user{i}', 'username': f'username{i}', 'password': f'password{i}'})
        # Create 1000 friendships
        for i in range(1000):
            self.app.post('/friendships', json={'user1_id': f'user{i}', 'user2_id': f'user{i+1}', 'rate_sharing': 'private'})
        # Create 1000 rated songs
        for i in range(1000):
            self.app.post('/rate_songs', json={'user_id': f'user{i}', 'song_id': f'song{i}', 'rating': 5})
        # Get 1000 friends recommendations
        start = time.time()
        for i in range(1000):
            self.app.get('/friends_recommendation', json={'user_id': f'user{i}'})
        end = time.time()
        print(f'Time taken to get 1000 friends recommendations: {end-start} seconds')
        # Delete 1000 rated songs
        for i in range(1000):
            self.app.delete('/rate_songs', json={'user_id': f'user{i}', 'song_id': f'song{i}'})
        # Delete 1000 friendships
        for i in range(1000):
            self.app.delete('/friendships', json={'user1_id': f'user{i}', 'user2_id': f'user{i+1}'})
        # Delete 1000 users
        for i in range(1000):
            self.app.delete('/users', json={'user_id': f'user{i}'})
            
            
if __name__ == '__main__':
    unittest.main()
