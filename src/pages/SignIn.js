import { useState } from "react";
import React from "react";
import { Link } from "react-router-dom";
import "../pagesCSS/SignIN-UP.css";

function SignIn() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPopup, setShowPopup] = useState(false); // State to control popup visibility

  const handleUserNameChange = (event) => {
    setEmail(event.target.value);
  };
  const handlePasswordChange = (event) => {
    setPassword(event.target.value);
  };

  const LogIn = () => {
    //LOGIN REQUEST WILL BE GET AND IF LOGIN IS TRUE THAN GO TO MAIN PAGE

    let json = {
      email: email,
      password: password,
    };
    console.log("LOGIN CLICKED");
    console.log(json);

    //VAR JSON WILL BE SEND AND isLogin will be received.

    let isLogin = false; //if isLogin is false
    if (isLogin) {
      //Than naviagte to main page
    }
    if (!isLogin) {
      //Than show pop-up login unsucessful!
      setShowPopup(true); // Show the popup
      setTimeout(() => setShowPopup(false), 3000);
    }
  };

  return (
    <div className="mcard-locat">
      <div className="m-card">
        <h1>Sign in</h1>
        <p className="details-register-p">
          Please enter your login and password!
        </p>
        {showPopup && (
          <div className="popup">
            <p>Login unsuccessful! Please try again!</p>
          </div>
        )}
        <input
          className="get-input"
          placeholder="Email address"
          type="email"
          onChange={handleUserNameChange}
        />
        <input
          className="get-input"
          placeholder="Password"
          type="password"
          onChange={handlePasswordChange}
        />

        <hr />

        <button className="button-log-reg" type="submit" onClick={LogIn}>
          Login
        </button>

        <p className="white-p">
          Don't have an account?{" "}
          <Link to="/signup" className="g-link">
            Register here
          </Link>
        </p>
        <p className="details-register-p">
          To sign in you need to have premium spotify account
        </p>
      </div>
    </div>
  );
}

export default SignIn;
