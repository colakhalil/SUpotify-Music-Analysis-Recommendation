import time
import unittest
from app import create_app, db  # Import your Flask app creation function

class TestUpdateFriendshipPerformance(unittest.TestCase):

    
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
    
    

         
 
"""    def TestAllUserDataPerformance (self):
        # Create 1000 users
        for i in range(1000):
            self.app.post('/users', json={'user_id': f'user{i}', 'username': f'username{i}', 'password': f'password{i}'})
        # Get all users
        start = time.time()
        self.app.get('/users')
        end = time.time()
        print(f'Time taken to get all users: {end-start} seconds')
        # Delete 1000 users
        for i in range(1000):
            self.app.delete('/users', json={'user_id': f'user{i}'}) """
if __name__ == '__main__':
    unittest.main()
