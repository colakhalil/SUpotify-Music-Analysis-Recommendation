import React from 'react';
import "../pagesCSS/tutorailpage.css";

const TutorialComponent = ({ setCurrentPlace }) => {
  // Your tutorial logic here

  const finishTutorial = () => {
    setCurrentPlace('main'); // Or any other place you want to navigate to after the tutorial
  };

  return (
    <div>
      <p>merhaba hello</p>
      
      <button onClick={finishTutorial}>Finish Tutorial</button>
    </div>
  );
};

export default TutorialComponent;
