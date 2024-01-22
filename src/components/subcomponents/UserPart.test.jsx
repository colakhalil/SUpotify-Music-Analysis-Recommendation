import React from 'react';
import { render } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import UserPart from './UserPart'; // Adjust the import path as needed

describe('UserPart Component', () => {
  const defaultProfilePic = "default-profile-pic-url.jpg";

  test('renders user information correctly', () => {
    const mockUserData = {
      username: 'testuser',
      profilePicture: 'test-profile-pic.jpg',
      friendsCount: 5
    };

    const { getByText, getByAltText } = render(<UserPart userData={mockUserData} />);

    expect(getByAltText(`${mockUserData.username}'s profile`)).toHaveAttribute('src', mockUserData.profilePicture);
    expect(getByText(mockUserData.username)).toBeInTheDocument();
    expect(getByText('5 Friends')).toBeInTheDocument();
  });

  test('renders default profile picture when not provided', () => {
    const mockUserData = {
      username: 'testuser',
      friendsCount: 1
    };

    const { getByAltText } = render(<UserPart userData={mockUserData} />);
    expect(getByAltText(`${mockUserData.username}'s profile`)).toHaveAttribute('src', defaultProfilePic);
  });

  test('renders nothing when userData is not provided', () => {
    const { container } = render(<UserPart userData={null} />);
    expect(container.firstChild).toBeNull();
  });

  // Additional tests can be added for different scenarios or additional features
});
