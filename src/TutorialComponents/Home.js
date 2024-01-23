import React from "react";

import Navbar from "./Navbar";
import { FiArrowRight } from "react-icons/fi";

const Home = ({setCurrentPlace}) => {
  return (
    <div className="home-container">
      <Navbar setCurrentPlace={setCurrentPlace}/>
      <div className="home-banner-container">

      <div className="work-section-top">
        <h1 className="primary-heading">Unlimited and Ad-Free Music</h1>
        <p className="primary-text">
            You're here for uninterrupted musical pleasure! Get ready for an ad-free, limitless music experience.
        </p>
      </div>
        

      </div>
    </div>
  );
};

export default Home;
