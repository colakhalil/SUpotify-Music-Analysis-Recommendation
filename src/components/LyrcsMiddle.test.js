import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import { act } from 'react-dom/test-utils'; // Import act
import '@testing-library/jest-dom/extend-expect';
import LyrcsMiddle from './LyrcsMiddle';

// Mock data for the song
const mockSong = {
  artists: 'Artist Name',
  title: 'Song Title',
  img: 'song-image-url.jpg'
};

// Setup a mock for fetch and console.error
beforeEach(() => {
  global.fetch = jest.fn().mockImplementation((url) => {
    if (url === `http://127.0.0.1:8008/lyrics/${mockSong.artists}/${mockSong.title}`) {
      return Promise.resolve({
        text: () => Promise.resolve("These are the lyrics \\n with some new lines \\n and unicode \\u00A0"),
      });
    }
    return Promise.reject(new Error('not found'));
  });

  global.console.error = jest.fn(); // Mock console.error
});

afterEach(() => {
  jest.restoreAllMocks();
});

describe('LyrcsMiddle Component', () => {
  test('renders and displays loading state', () => {
    render(<LyrcsMiddle song={mockSong} />);
    const loadingElement = screen.getByText(/loading.../i);
    expect(loadingElement).toBeInTheDocument();
  });

  test('fetches and displays lyrics', async () => {
    await act(async () => {
      render(<LyrcsMiddle song={mockSong} />);
    });
    
    await waitFor(() => {
      expect(screen.getByText(/These are the lyrics with some new lines and unicode/)).toBeInTheDocument();
    });
  });

  test('displays error message when fetch fails', async () => {
    global.fetch.mockImplementationOnce(() => Promise.reject(new Error('Fetch failed')));

    await act(async () => {
      render(<LyrcsMiddle song={mockSong} />);
    });
    
    await waitFor(() => {
      expect(global.console.error).toHaveBeenCalledWith("Error fetching lyrics:", expect.any(Error));
    });
  });
});
