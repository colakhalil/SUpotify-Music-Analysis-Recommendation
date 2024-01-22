import React from 'react';
import { render } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import SongDetails from './SongDetails'; // Adjust the import path as needed

describe('SongDetails Component', () => {
  const mockSong = {
    thumbnail: 'thumbnail_url.jpg',
    title: 'Test Song',
    artists: 'Test Artist',
    genre: 'Pop',
    album_id: '12345'
  };

  test('renders song details correctly', () => {
    const { getByText, getByAltText } = render(<SongDetails song={mockSong} />);

    const image = getByAltText('Test Song album cover');
    expect(image).toHaveAttribute('src', mockSong.thumbnail);

    expect(getByText(mockSong.title)).toBeInTheDocument();
    expect(getByText(mockSong.artists)).toBeInTheDocument();
    expect(getByText(`Genre: ${mockSong.genre}`)).toBeInTheDocument();
    expect(getByText(mockSong.album_id)).toBeInTheDocument();
  });

  // Additional tests can be written to cover different scenarios or additional features of the component
});
