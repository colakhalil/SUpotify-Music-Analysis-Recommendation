import React from 'react';
import { render, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import RecommendArtist from './RecommendArtist'; // Adjust the import path as needed

// Mock global fetch
global.fetch = jest.fn();

beforeEach(() => {
  fetch.mockClear();
});

describe('RecommendArtist Component', () => {
  const mockUserId = 'user123';

  test('renders correctly and fetches artist recommendations', async () => {
    const mockRecommendations = [
      { artist_id: '1', artist_name: 'Artist One', picture: 'url1' },
      { artist_id: '2', artist_name: 'Artist Two', picture: 'url2' }
    ];

    fetch.mockResolvedValueOnce({
      json: () => Promise.resolve({ recommendations: mockRecommendations })
    });

    const { getByText, getAllByRole } = render(<RecommendArtist currentUserId={mockUserId} />);

    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith(`http://127.0.0.1:8008/${mockUserId}/friend_artist_recommendations`);
      expect(getByText('Artist One')).toBeInTheDocument();
      expect(getByText('Artist Two')).toBeInTheDocument();
    });

    const images = getAllByRole('img');
    expect(images[0]).toHaveAttribute('src', 'url1');
    expect(images[1]).toHaveAttribute('src', 'url2');
  });

  // You can add more tests to cover error handling or different response scenarios
});
