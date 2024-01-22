import React from 'react';
import { render, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import SongOptions from './SongOptions'; // Adjust the import path as needed

describe('SongOptions Component', () => {
  test('renders lyrics button and triggers event on click', () => {
    const mockToggleLyrics = jest.fn();
    const { getByText } = render(<SongOptions toggleLyrics={mockToggleLyrics} />);

    const lyricsButton = getByText('Lyrics');
    expect(lyricsButton).toBeInTheDocument();

    fireEvent.click(lyricsButton);
    expect(mockToggleLyrics).toHaveBeenCalledTimes(1);
  });

  // Additional tests can be added for other functionalities or scenarios
});
