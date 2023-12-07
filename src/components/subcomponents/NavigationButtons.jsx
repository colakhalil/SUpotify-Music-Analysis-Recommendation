import React from "react";

const NavigationButtons = ({ onHomeClick, onSearchClick, onProfileClick,onDatabaseClick }) => {
  return (
    <>
      <button className="left-bar-button" onClick={onHomeClick}>
        Main Page
      </button>
      <button className="left-bar-button" onClick={onProfileClick}>
        Profile
      </button>
      <button className="left-bar-button" onClick= {onDatabaseClick}>Database</button>
    </>
  );
};

export default NavigationButtons;
