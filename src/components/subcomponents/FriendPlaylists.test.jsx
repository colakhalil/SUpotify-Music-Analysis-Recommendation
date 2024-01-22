import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import FriendPlaylists from './FriendPlaylists'; // Adjust the import path as necessary

describe('FriendPlaylists Component', () => {
  const mockName = 'Chill Vibes';
  const mockThumbnail = 'https://example.com/thumbnail.jpg';
  const mockOnClick = jest.fn();

  it('renders the playlist information correctly', () => {
    render(<FriendPlaylists name={mockName} thumbnail={mockThumbnail} onClick={mockOnClick} />);

    // Check if the name is rendered
    expect(screen.getByText(mockName)).toBeInTheDocument();

    // Check if the thumbnail is rendered with correct src and alt attributes
    const image = screen.getByRole('img', { name: `Playlist: ${mockName}` });
    expect(image).toHaveAttribute('src', mockThumbnail);
    expect(image).toHaveAttribute('alt', `Playlist: ${mockName}`);
  });

  it('handles click event correctly', () => {
    render(<FriendPlaylists name={mockName} thumbnail={mockThumbnail} onClick={mockOnClick} />);

    // Simulate user clicking on the playlist item
    fireEvent.click(screen.getByText(mockName));

    // Check if the onClick handler was called
    expect(mockOnClick).toHaveBeenCalled();
  });

  // Additional tests can be added to cover other scenarios
});
