import { useState } from "react";
import React from "react";
import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";
import { Link, useNavigate } from "react-router-dom";
import "../pagesCSS/SignIN-UP.css";
function SignUp() {
  const [username, setUsernamen] = useState("");
  const [emailn, setEmailn] = useState("");
  const [passwordn, setPasswordn] = useState("");
  const [confirmPassword,setConfirmPassword] = useState("");
  const [userData, setUserData] = useState([]); //dummy json
  const [showPopup, setShowPopup] = useState(false); // State to control popup visibility
  const navigate = useNavigate();
  const Register = () => {
    let json = {
      email: emailn,
      password: passwordn,
      username: username,
    };
    console.log(json);

    //VAR JSON WILL BE SEND AND isRegister will be received.

    let isRegister = true; //if isRegister is false
    if (isRegister) {
      //Than naviagte to main page
      navigate("/main");
    }
    if (!isRegister) {
      //Than show pop-up register unsucessful!
      setShowPopup(true); // Show the popup
      setTimeout(() => setShowPopup(false), 3000);
    }
  };

  const handleSignUpClick = () => {
    if (passwordn !== confirmPassword) {
      alert('The two passwords must match.'); // Parolalar eşleşmiyorsa bir uyarı gösterin.
    } else {
      //kullanıcı verisi json'a kaydetmek için
      const newUser = { username, emailn, passwordn };
      setUserData([...userData, newUser]);
      alert('Registration Succesfull!') //test amaçlı doğrulama mesajı
      // Burada parolalar eşleştiğinde yapılacak işlemler yer alacak.
      // Örneğin bir API'ye kayıt isteği gönderebilirsiniz.
    }
  };

  const handleEmailChange = (event) => {
    setEmailn(event.target.value);
  };

  const handleUserNameChange = (event) => {
    setUsernamen(event.target.value);
  };
  const handlePasswordChange = (event) => {
    setPasswordn(event.target.value);
  };

  const handleConfirmPasswordChange = (event) => {
    setConfirmPassword(event.target.value);
  };
  return (
    <div className="mcard-locat">
      <div className="m-card">
        <h1>Sign Up</h1>
        <p className="details-register-p">
          Please enter your details to register!
        </p>
        {showPopup && (
          <div className="popup">
            <p>Register unsuccessful! Please try again!</p>
          </div>
        )}
        <input
          className="get-input"
          placeholder="Username"
          type="usernamen"
          onChange={handleUserNameChange}
        />
        <input
          className="get-input"
          placeholder="Email Address"
          type="emailn"
          onChange={handleEmailChange}
        />
        <input
          className="get-input"
          placeholder="Password"
          type="password"
          onChange={handlePasswordChange}
        />
        <input
        className="get-input"
        onChange={handleConfirmPasswordChange}
        placeholder="Confirm Password"
        type="password"
        value={confirmPassword}
        />

        <hr />

        <button type="submit" className="button-log-reg" onClick={Register}>
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