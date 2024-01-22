import React from 'react';
import { render, waitFor, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import fetchMock from 'jest-fetch-mock';
import MonthlyAverageRatingsChart from './MonthlyAverageRatingsChart'; // Adjust the import path as necessary
import globalVar from '../../global.js'; // Adjust the import path as necessary

fetchMock.enableMocks();

beforeEach(() => {
  fetch.resetMocks();
});

describe('MonthlyAverageRatingsChart Component', () => {
  it('fetches and displays monthly average ratings', async () => {
    const mockData = {
      monthly_average_ratings: [
        { year: 2023, month: 1, average_rating: 4.5 },
        { year: 2023, month: 2, average_rating: 4.2 },
        // Add more mock data as needed
      ],
    };

    fetch.mockResponseOnce(JSON.stringify(mockData));

    render(<MonthlyAverageRatingsChart />);

    // Wait for the component to finish loading data
    await waitFor(() => {
      // Check for specific data points in your component
      expect(screen.getByText("2023-01")).toBeInTheDocument();
      expect(screen.getByText("2023-02")).toBeInTheDocument();

      // Additional checks can be added for other elements like LineChart
    });
  });

  // Additional tests can be added to cover other scenarios, like error handling
});
