import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import SongRating from './SongRating'; // Adjust the import path as necessary

describe('SongRating Component', () => {
  // Test for checking if the component renders with initial user rating
  it('renders with given user rating', () => {
    render(<SongRating userRating={3} onRatingChange={() => {}} />);
    const filledStars = screen.getAllByText('★').slice(0, 3);
    filledStars.forEach(star => {
      expect(star).toHaveStyle('color: rgb(255, 215, 0)'); // Checking if the stars are filled (assuming filled stars are yellow)
    });
  });

  // Test for simulating a rating change
  it('calls onRatingChange when a new rating is clicked', () => {
    const mockOnRatingChange = jest.fn();
    render(<SongRating userRating={3} onRatingChange={mockOnRatingChange} />);
    
    const stars = screen.getAllByText('★');
    const newRatingStar = stars[4]; // Select the fifth star
    fireEvent.click(newRatingStar);
    expect(mockOnRatingChange).toHaveBeenCalledWith(5);
  });
});
