import React from 'react';

const NavigationButtons = ({ onHomeClick, onSearchClick }) => {
  return (
    <>
      <button className="left-bar-button" onClick={onHomeClick}>
        Main Page
      </button>
      <button className="left-bar-button" onClick={onSearchClick}>
        Profile
      </button>
      <button className="left-bar-button">
        Library
      </button>
    </>
  );
};

export default NavigationButtons;
