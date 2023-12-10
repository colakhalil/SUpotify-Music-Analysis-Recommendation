import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import PlaylistItemLeftbar from './PlaylistItemLeftbar'; // Adjust the import path as necessary

describe('PlaylistItemLeftbar Component', () => {
  const mockPlaylist = {
    playlistID: '123',
    playlistPic: 'test-pic-url',
    name: 'Test Playlist',
    songNumber: 5
  };

  // Test for checking if the component displays the playlist information
  it('displays the correct playlist information', () => {
    render(<PlaylistItemLeftbar playlist={mockPlaylist} onClick={() => {}} />);
    
    expect(screen.getByAltText('Test Playlist')).toHaveAttribute('src', 'test-pic-url');
    expect(screen.getByText('Test Playlist')).toBeInTheDocument();
    expect(screen.getByText('5 songs')).toBeInTheDocument();
  });

  // Test for checking the onClick function with the correct playlist ID
  it('calls onClick with the correct playlist ID when clicked', () => {
    const mockOnClick = jest.fn();
    render(<PlaylistItemLeftbar playlist={mockPlaylist} onClick={mockOnClick} />);
    
    const playlistButton = screen.getByRole('button');
    fireEvent.click(playlistButton);
    expect(mockOnClick).toHaveBeenCalledWith('123');
  });

  // Add more tests here if needed
});
