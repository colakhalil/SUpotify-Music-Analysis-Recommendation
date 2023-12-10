import React from 'react';
import { render, fireEvent, screen } from '@testing-library/react';
import { BrowserRouter as Router } from 'react-router-dom'; // Import Router from react-router-dom
import SignUp from './SignUp'; // Import your SignUp component

// ... your test code ...


// Mock any dependencies or context providers if needed

describe('SignUp component', () => {
  it('should render the signup form and submit the form', () => {
    // Render the SignUp component
    render(
      <Router>
        <SignUp />
      </Router>
    );

    // Fill in the form fields
    const usernameInput = screen.getByLabelText('Username');
    const emailInput = screen.getByLabelText('Email Address');
    const passwordInput = screen.getByLabelText('Password');
    const confirmPasswordInput = screen.getByLabelText('Confirm Password');

    fireEvent.change(usernameInput, { target: { value: 'testuser' } });
    fireEvent.change(emailInput, { target: { value: 'test@example.com' } });
    fireEvent.change(passwordInput, { target: { value: 'password123' } });
    fireEvent.change(confirmPasswordInput, { target: { value: 'password123' } });

    // Submit the form
    const submitButton = screen.getByText('Register');
    fireEvent.click(submitButton);

    // Assert that the form was submitted correctly (you might customize this based on your implementation)
    expect('Assert that the form was submitted correctly').toBeTruthy();
  });
});
