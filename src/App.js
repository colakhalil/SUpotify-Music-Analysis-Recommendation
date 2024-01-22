import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import SignIn from "./pages/SignIn";
import SignUp from "./pages/SignUp";
import MainPage from "./pages/MainPage";
import TutorialComponent from "./pages/TutorialComponent";


function App() {
  return (
    <Router>
      <Routes>
        <Route exact path="/" element={<SignIn></SignIn>} />
        <Route exact path="/signup" element={<SignUp></SignUp>} />
        <Route exact path="/main" element={<MainPage></MainPage>} />
        <Route exact path="/tutorial" element={<TutorialComponent></TutorialComponent>} />
      </Routes>
    </Router>
  );
}

export default App;
