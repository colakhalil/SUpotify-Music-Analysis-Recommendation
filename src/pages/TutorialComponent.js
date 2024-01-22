import "../pagesCSS/TutorialPage.css";
import Home from "../TutorialComponents/Home";
import About from "../TutorialComponents/About";
import Work from "../TutorialComponents/Work";
import Testimonial from "../TutorialComponents/Testimonial";
import Contact from "../TutorialComponents/Contact";
import Footer from "../TutorialComponents/Footer";

const TutorialComponent = ({ setCurrentPlace}) => {
  const finishTutorial = () => {
    setCurrentPlace('main'); // Or any other place you want to navigate to after the tutorial
  };
  return (
    <div className="App">
      <Home />
      <Work />

    </div>
  );

};

export default TutorialComponent;

