import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

const SignupPage = () => {
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    password: ""
  });
  const [message, setMessage] = useState("");
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

//   sending data to backend and storing token in localStorage
  const handleSignup = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post("https://activity6vishvesh.onrender.com/api/auth/register", formData);
      localStorage.setItem("token", response.data.token);
      setMessage("Signup successful! Token saved.");
      setTimeout(() => {
        // navigating to login 
        navigate("/login");
      }, 1000);
    } catch (err) {
      setMessage(err.response?.data?.error || "Signup failed.");
    }
  };

  return (
    <div className="container mt-5">
      <h2>Sign Up</h2>
      {message && <p className="mt-3">{message}</p>}
      <form onSubmit={handleSignup}>
        <input type="text" name="name" placeholder="Full Name" value={formData.name} onChange={handleChange} className="form-control mb-3" />
        <input type="email" name="email" placeholder="Email" value={formData.email} onChange={handleChange} className="form-control mb-3" />
        <input type="password" name="password" placeholder="Password" value={formData.password} onChange={handleChange} className="form-control mb-3" />
        <button type="submit" className="btn btn-primary">Sign Up</button>
      </form>
      
    </div>
  );
};

export default SignupPage;
