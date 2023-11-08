import React from 'react';

const NavigationButtons = ({ onHomeClick, onSearchClick }) => {
  return (
    <>
      <button className="left-bar-button" onClick={onHomeClick}>
        Ana sayfa
      </button>
      <button className="left-bar-button" onClick={onSearchClick}>
        Profil
      </button>
      <button className="left-bar-button">
        Kitaplığın
      </button>
    </>
  );
};

export default NavigationButtons;
