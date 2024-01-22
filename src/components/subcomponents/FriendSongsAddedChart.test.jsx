import React from 'react';
import { render, waitFor, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import fetchMock from 'jest-fetch-mock';
import FriendSongsAddedChart from './FriendSongsAddedChart'; // Adjust the import path as necessary
import globalVar from '../../global.js'; // Adjust the import path as necessary

fetchMock.enableMocks();

beforeEach(() => {
  fetch.resetMocks();
});

describe('FriendSongsAddedChart Component', () => {
  it('fetches and displays data correctly', async () => {
    const mockData = [
      { artist_name: 'Artist 1', song_count: 10 },
      { artist_name: 'Artist 2', song_count: 15 },
      // Add more mock data as needed
    ];

    fetch.mockResponseOnce(JSON.stringify(mockData));

    render(<FriendSongsAddedChart />);

    // Wait for the component to finish loading data
    await waitFor(() => {
      // Check for specific data points in your component
      expect(screen.getByText('Artist 1')).toBeInTheDocument();
      expect(screen.getByText('Artist 2')).toBeInTheDocument();

      // Additional checks can be added for other elements like BarChart
    });
  });

  // Additional tests can be added to cover other scenarios, like error handling
});
