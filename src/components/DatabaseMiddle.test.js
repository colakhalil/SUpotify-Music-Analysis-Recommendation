import React from 'react';
import { render, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import DatabaseMiddle from './DatabaseMiddle'; // Adjust the import path as needed
import PlaylistContainer from './subcomponents/PlaylistContainer'; // Adjust as needed
import globalVar from '../global.js'; // Adjust as needed

// Mock global fetch
global.fetch = jest.fn();

jest.mock('./subcomponents/PlaylistContainer', () => {
  return ({ songs, setCurrentBottomSong }) => (
    <div data-testid="mock-playlist-container">
      Mocked Playlist Container
    </div>
  );
});

describe('DatabaseMiddle Component', () => {
  beforeEach(() => {
    fetch.mockClear();
  });

  test('fetches songs and renders PlaylistContainer', async () => {
    const mockSongs = [
      { song_name: 'Song 1', artist_name: 'Artist 1', duration: '3:30', release_date: '2020', rate: 4, song_id: '1' },
      // Add more mock songs as needed
    ];

    fetch.mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve({ songs: mockSongs }),
    });

    const { getByTestId } = render(<DatabaseMiddle setCurrentBottomSong={() => {}} dataBaseChanged={false} />);

    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith(`http://127.0.0.1:8008/${globalVar.username}/all_songs`);
      expect(getByTestId('mock-playlist-container')).toBeInTheDocument();
    });
  });

  // Additional tests can be added for error handling, effect dependency, and different scenarios
});
