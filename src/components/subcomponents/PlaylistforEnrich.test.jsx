import React from 'react';
import { render, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import PlaylistforEnrich from './PlaylistforEnrich';
import EnrichButton from './EnrichButton'; // Adjust the import path if necessary

// Mock the EnrichButton component
jest.mock('./EnrichButton', () => {
  // Mock component with props and a click handler
  return ({ onEnrich }) => (
    <button onClick={() => onEnrich([{ song_id: '1', song_name: 'Test Song', artist_name: ['Test Artist'] }])}>
      Mock Enrich Button
    </button>
  );
});

describe('PlaylistforEnrich Component', () => {
  test('renders correctly with EnrichButton', () => {
    const { getByText } = render(<PlaylistforEnrich userId="123" genre="rock" />);
    expect(getByText('Mock Enrich Button')).toBeInTheDocument();
  });

  test('enriches and displays new songs', () => {
    const { getByText, getAllByRole } = render(<PlaylistforEnrich userId="123" genre="rock" />);
    const enrichButton = getByText('Mock Enrich Button');
    fireEvent.click(enrichButton);

    const listItems = getAllByRole('listitem');
    expect(listItems.length).toBe(1);
    expect(listItems[0]).toHaveTextContent('Test Song - Test Artist');
  });
});
