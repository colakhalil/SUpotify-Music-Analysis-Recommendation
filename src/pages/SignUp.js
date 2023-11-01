import { useState } from "react";
import React from "react";
import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";
import { Link } from "react-router-dom";
import "../pagesCSS/SignIN-UP.css";
function SignUp() {
  const [username, setUsernamen] = useState("");
  const [emailn, setEmailn] = useState("");
  const [passwordn, setPasswordn] = useState("");

  return (
    <div className="mcard-locat">
      <div className="m-card">
        <h1>Sign Up</h1>
        <p className="details-register-p">
          Please enter your details to register!
        </p>

        <input
          className="get-input"
          onClick={() => setUsernamen("")}
          placeholder="Username"
          type="usernamen"
        />
        <input
          className="get-input"
          onClick={() => setEmailn("")}
          placeholder="Email Address"
          type="emailn"
        />
        <input
          className="get-input"
          onClick={() => setPasswordn("")}
          placeholder="Password"
          type="passwordn"
        />

        <hr />

        <button type="submit" className="button-log-reg">
          Register
        </button>

        <p className="white-p">
          have an account?{" "}
          <Link to="/" className="g-link">
            sign in here
          </Link>
        </p>
        <p className="details-register-p">
          To sign up you need to have premium spotify account
        </p>
      </div>
    </div>
  );
}

export default SignUp;
