import React from 'react';
import { render } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import TopSongsChart from './TopSongsChart'; // Adjust the import path as needed

describe('TopSongsChart Component', () => {
  const mockTopSongs = [
    { title: 'Song 1', plays: 150 },
    { title: 'Song 2', plays: 120 },
    { title: 'Song 3', plays: 100 }
  ];

  test('renders top songs correctly', () => {
    const { getByText } = render(<TopSongsChart topSongs={mockTopSongs} />);

    // Check if each song is rendered with correct details
    mockTopSongs.forEach((song, index) => {
      expect(getByText(`#${index + 1}`)).toBeInTheDocument();
      expect(getByText(song.title)).toBeInTheDocument();
      expect(getByText(`Plays: ${song.plays}`)).toBeInTheDocument();
    });

    // Additional checks can be made for the structure and style of the list
  });

  // Additional tests can be added for different scenarios or additional features
});
