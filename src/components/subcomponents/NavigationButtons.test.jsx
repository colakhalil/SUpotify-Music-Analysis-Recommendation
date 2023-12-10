import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import NavigationButtons from './NavigationButtons'; // Adjust the import path as necessary

describe('NavigationButtons Component', () => {
  // Test for Main Page button click
  it('calls onHomeClick when the Main Page button is clicked', () => {
    const mockOnHomeClick = jest.fn();
    render(<NavigationButtons onHomeClick={mockOnHomeClick} onSearchClick={() => {}} onProfileClick={() => {}} onDatabaseClick={() => {}} />);
    
    const mainPageButton = screen.getByText('Main Page');
    fireEvent.click(mainPageButton);
    expect(mockOnHomeClick).toHaveBeenCalled();
  });

  // Test for Profile button click
  it('calls onProfileClick when the Profile button is clicked', () => {
    const mockOnProfileClick = jest.fn();
    render(<NavigationButtons onHomeClick={() => {}} onSearchClick={() => {}} onProfileClick={mockOnProfileClick} onDatabaseClick={() => {}} />);
    
    const profileButton = screen.getByText('Profile');
    fireEvent.click(profileButton);
    expect(mockOnProfileClick).toHaveBeenCalled();
  });

  // Test for Database button click
  it('calls onDatabaseClick when the Database button is clicked', () => {
    const mockOnDatabaseClick = jest.fn();
    render(<NavigationButtons onHomeClick={() => {}} onSearchClick={() => {}} onProfileClick={() => {}} onDatabaseClick={mockOnDatabaseClick} />);
    
    const databaseButton = screen.getByText('Database');
    fireEvent.click(databaseButton);
    expect(mockOnDatabaseClick).toHaveBeenCalled();
  });
});
