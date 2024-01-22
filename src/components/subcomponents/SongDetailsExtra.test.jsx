import React from 'react';
import { render } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import SongDetailsExtra from './SongDetailsExtra'; // Adjust the import path as needed

describe('SongDetailsExtra Component', () => {
  const mockSong = {
    playCount: '123',
    releaseYear: '2020',
    dateAdded: '2021-01-01'
  };

  test('renders song extra details correctly', () => {
    const { getByText } = render(<SongDetailsExtra song={mockSong} />);

    expect(getByText(`Plays: ${mockSong.playCount}`)).toBeInTheDocument();
    expect(getByText(`Release: ${mockSong.releaseYear}`)).toBeInTheDocument();
    expect(getByText(`Added: ${mockSong.dateAdded}`)).toBeInTheDocument();
  });

  // Additional tests can be written to cover different scenarios or additional features of the component
});
