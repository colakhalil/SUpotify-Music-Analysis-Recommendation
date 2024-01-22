import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import Playlist from './Playlist'; // Adjust the import path as necessary

describe('Playlist Component', () => {
  const mockName = 'Summer Hits';
  const mockThumbnail = 'https://example.com/cover.jpg';
  const mockOnClick = jest.fn();

  it('renders the playlist information correctly', () => {
    render(
      <Playlist
        name={mockName}
        thumbnail={mockThumbnail}
        onClick={mockOnClick}
      />
    );

    // Check if the name is rendered
    expect(screen.getByText(mockName)).toBeInTheDocument();

    // Check if the thumbnail is rendered with correct src and alt attributes
    const image = screen.getByRole('img', { name: `${mockName} cover` });
    expect(image).toHaveAttribute('src', mockThumbnail);
    expect(image).toHaveAttribute('alt', `${mockName} cover`);
  });

  it('handles click event correctly', () => {
    render(
      <Playlist
        name={mockName}
        thumbnail={mockThumbnail}
        onClick={mockOnClick}
      />
    );

    // Simulate user clicking on the playlist
    fireEvent.click(screen.getByText(mockName));

    // Check if the onClick handler was called
    expect(mockOnClick).toHaveBeenCalled();
  });

  // Additional tests can be added to cover other scenarios
});
