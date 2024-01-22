import React from 'react';
import { render } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import UserPlaylists from './UserPlaylists'; // Adjust the import path as needed

describe('UserPlaylists Component', () => {
  test('renders playlist cards correctly', () => {
    const mockPlaylists = [
      { name: 'Playlist 1', thumbnail: 'thumbnail1.jpg' },
      { name: 'Playlist 2', thumbnail: 'thumbnail2.jpg' }
    ];

    const { getByText } = render(<UserPlaylists playlists={mockPlaylists} />);

    expect(getByText('Playlist 1')).toBeInTheDocument();
    expect(getByText('Playlist 2')).toBeInTheDocument();

    // Check the background-image style of the playlist-thumbnail divs instead of img tags
    const playlistThumbnails = document.querySelectorAll('.playlist-thumbnail');
    expect(playlistThumbnails[0]).toHaveStyle(`background-image: url(${mockPlaylists[0].thumbnail})`);
    expect(playlistThumbnails[1]).toHaveStyle(`background-image: url(${mockPlaylists[1].thumbnail})`);
  });

  // Additional tests can be added for different scenarios or additional features
});
