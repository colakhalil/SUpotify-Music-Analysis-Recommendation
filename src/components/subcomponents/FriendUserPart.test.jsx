import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import FriendUserPart from './FriendUserPart'; // Adjust the import path as necessary

describe('FriendUserPart Component', () => {
  const mockFriendData = {
    friendName: 'Alice',
    profilePicture: 'https://example.com/profile.jpg',
    numberOfFriends: 5
  };

  it('renders the user information correctly', () => {
    render(<FriendUserPart friendData={mockFriendData} />);

    // Check if the name and friend count are rendered
    expect(screen.getByText('Alice')).toBeInTheDocument();
    expect(screen.getByText('5 Friends')).toBeInTheDocument();

    // Check if the profile picture is rendered with the correct src and alt attributes
    const image = screen.getByRole('img', { name: `${mockFriendData.friendName}'s profile` });
    expect(image).toHaveAttribute('src', mockFriendData.profilePicture);
    expect(image).toHaveAttribute('alt', `${mockFriendData.friendName}'s profile`);
  });

  it('handles add friend button click', () => {
    // Mock the console.log function
    const consoleSpy = jest.spyOn(console, 'log');

    render(<FriendUserPart friendData={mockFriendData} />);

    // Simulate clicking the 'Add Friend' button
    fireEvent.click(screen.getByText('Add Friend'));

    // Check if the console.log was called with the correct message
    expect(consoleSpy).toHaveBeenCalledWith('Add friend clicked');
  });

  it('handles remove friend button click', () => {
    // Mock the console.log function
    const consoleSpy = jest.spyOn(console, 'log');

    render(<FriendUserPart friendData={mockFriendData} />);

    // Simulate clicking the 'Remove Friend' button
    fireEvent.click(screen.getByText('Remove Friend'));

    // Check if the console.log was called with the correct message
    expect(consoleSpy).toHaveBeenCalledWith('Remove friend clicked');
  });

  // Additional tests can be added to cover other scenarios
});
