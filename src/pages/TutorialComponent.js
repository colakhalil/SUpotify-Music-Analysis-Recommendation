import "../pagesCSS/TutorialPage.css";
import Home from "../TutorialComponents/Home";
import About from "../TutorialComponents/About";
import Work from "../TutorialComponents/Work";
import Testimonial from "../TutorialComponents/Testimonial";
import Contact from "../TutorialComponents/Contact";
import Footer from "../TutorialComponents/Footer";

const TutorialComponent = ({ setCurrentPlace}) => {

  return (
    <div className="App">
      <Home setCurrentPlace= {setCurrentPlace}/>
      <Work />

    </div>
  );

};

export default TutorialComponent;

