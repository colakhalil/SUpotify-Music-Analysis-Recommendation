import React from 'react';
import { BrowserRouter as Router, Route ,Routes} from 'react-router-dom'; 
import SignIn from './SignIn';
import SignUp from './SignUp';
import './App.css';

// Diğer bileşenleri içe aktarın

function App() {
  return (
    <Router>
      <Routes>
        <Route exact path="/" element={<SignIn></SignIn>} />
        <Route exact path="/signup" element={<SignUp></SignUp>} />
      </Routes>
    </Router>
  );
}

export default App;
