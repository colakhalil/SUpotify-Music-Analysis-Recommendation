import { useState } from "react";
import React from "react";
import { Link } from "react-router-dom";
import "../pagesCSS/SignIN-UP.css";

function SignIn() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  return (
    <div className="mcard-locat">
      <div className="m-card">
        <h1>Sign in</h1>
        <p className="details-register-p">
          Please enter your login and password!
        </p>

        <input
          className="get-input"
          onClick={() => setEmail("")}
          placeholder="Email address"
          type="email"
        />
        <input
          className="get-input"
          onClick={() => setPassword("")}
          placeholder="Password"
          type="password"
        />

        <hr />

        <button className="button-log-reg" type="submit">
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
