import { useState } from "react";
import React from "react";
import { Link, useNavigate } from "react-router-dom";
import "../pagesCSS/SignIN-UP.css";

function SignIn() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPopup, setShowPopup] = useState(false); // State to control popup visibility
  const navigate = useNavigate();
  const handleUserNameChange = (event) => {
    setEmail(event.target.value);
  };
  const handlePasswordChange = (event) => {
    setPassword(event.target.value);
  };
  const LogIn = async () => {
    let json = {
      email: email,
      password: password,
    };
    console.log(json);
    let isLogin = true;
    try {
      const response = await fetch("http://127.0.0.1:8008/login", {
        method: "POST", // or 'PUT' if your backend requires
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(json),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      isLogin = data["message"]; //if isLogin is false
      console.log("Success:", data);
      // Handle the response data in here
    } catch (error) {
      console.error("Error:", error);
    }
    console.log("islogin: ", isLogin);
    if (isLogin) {
      //Than naviagte to main page
      navigate("/main");
    }
    if (!isLogin) {
      //Than show pop-up register unsucessful!
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
