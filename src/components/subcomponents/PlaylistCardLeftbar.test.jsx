import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import PlaylistCardLeftbar from './PlaylistCardLeftbar'; // Adjust the import path as necessary
import PlaylistItemLeftbar from './PlaylistItemLeftbar'; // Adjust the import path as necessary

// Mock the PlaylistItemLeftbar component
jest.mock('./PlaylistItemLeftbar', () => (props) => (
  <div data-testid="playlist-item" onClick={props.onClick}>
    {props.playlist.name}
  </div>
));

describe('PlaylistCardLeftbar Component', () => {
  const mockPlaylists = [
    { playlistID: '1', name: 'Playlist 1' },
    { playlistID: '2', name: 'Playlist 2' },
    // Add more mock playlists as needed
  ];
  const mockOnPlaylistClick = jest.fn();

  it('renders multiple PlaylistItemLeftbar components', () => {
    render(
      <PlaylistCardLeftbar
        playlists={mockPlaylists}
        onPlaylistClick={mockOnPlaylistClick}
      />
    );

    // Check if the correct number of PlaylistItemLeftbar components are rendered
    const playlistItems = screen.getAllByTestId('playlist-item');
    expect(playlistItems).toHaveLength(mockPlaylists.length);

    // Check if each PlaylistItemLeftbar component displays the correct name
    mockPlaylists.forEach((playlist, index) => {
      expect(playlistItems[index]).toHaveTextContent(playlist.name);
    });
  });

  it('handles click event on each PlaylistItemLeftbar correctly', () => {
    render(
      <PlaylistCardLeftbar
        playlists={mockPlaylists}
        onPlaylistClick={mockOnPlaylistClick}
      />
    );

    // Simulate clicks on each PlaylistItemLeftbar
    mockPlaylists.forEach((playlist, index) => {
      fireEvent.click(screen.getAllByTestId('playlist-item')[index]);
    });

    // Check if the onPlaylistClick handler was called the correct number of times
    expect(mockOnPlaylistClick).toHaveBeenCalledTimes(mockPlaylists.length);
  });

  // Additional tests can be added to cover other scenarios
});
