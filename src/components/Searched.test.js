import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import UserList from './Searched';
import globalVar from "../global.js";



// Mock data for users and friends
const users = [
  { user_id: 'user1', profile_pic: 'profile-pic1.png' },
  { user_id: 'user2', profile_pic: 'profile-pic2.png' }
];
const friendsData = [{ name: 'user1' }];

// Mocking the global variable
globalVar.username = 'current_user';

// Setup a mock for fetch
beforeEach(() => {
    global.fetch = jest.fn((url, options) =>
      Promise.resolve({
        json: () => {
          // You can add logic here to return different responses based on the URL or options
          if (options.method === 'POST') {
            if (url.includes('add_friend')) {
              return Promise.resolve({ message: 'Friend added successfully' });
            } else if (url.includes('remove_friend')) {
              return Promise.resolve({ message: 'Friend removed successfully' });
            }
          }
          // Default response for GET or any other requests
          return Promise.resolve([]);
        },
      })
    );
  });
  
// Reset the mocks after each test
afterEach(() => {
    jest.restoreAllMocks();
  });



describe('UserList Component', () => {
  // Resets the fetch mock before each test
  beforeEach(() => {
    fetch.mockClear();
  });

  it('renders without crashing', () => {
    render(<UserList users={users} friendsData={friendsData} />);
  });

  it('contains a search input', () => {
    render(<UserList users={users} friendsData={friendsData} />);
    expect(screen.getByPlaceholderText('Search...')).toBeInTheDocument();
  });

  it('adds a friend', async () => {
    const setFriendsUpdate = jest.fn();
    render(<UserList users={users} friendsData={friendsData} setFriendsUpdate={setFriendsUpdate} />);
    
    fireEvent.click(screen.getByText('Add'));
    
    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith(expect.stringContaining('/add_friend/'), expect.anything());
    });
  });

  it('removes a friend', async () => {
    const setFriendsUpdate = jest.fn();
    render(<UserList users={users} friendsData={friendsData} setFriendsUpdate={setFriendsUpdate} friendsUpdate={false} />);
    
    fireEvent.click(screen.getByText('Remove'));
    
    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith(expect.stringContaining('/remove_friend/'), expect.anything());
    });
  });
});
