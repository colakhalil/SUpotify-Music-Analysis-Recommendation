import React from 'react';

const TutorialComponent = ({ setCurrentPlace }) => {
  // Your tutorial logic here

  const finishTutorial = () => {
    setCurrentPlace('main'); // Or any other place you want to navigate to after the tutorial
  };

  return (
    <div>
      {/* Your tutorial content */}
      <button onClick={finishTutorial}>Finish Tutorial</button>
    </div>
  );
};

export default TutorialComponent;
