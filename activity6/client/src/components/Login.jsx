import React, { useState } from "react";
import axios from "axios";

const LoginPage = () => {
  const [formData, setFormData] = useState({ email: "", password: "" });
  const [message, setMessage] = useState("");

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

// sending data to backend and storing token in localStorage
  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post("http://localhost:5000/api/auth/login", formData);
      localStorage.setItem("token", response.data.token);
      setMessage("Login successful! Token saved.");
    } catch (err) {
      setMessage(err.response?.data?.error || "Login failed.");
    }
  };

  return (
    <div className="container mt-5">
      <h2>Login</h2>
       {message && <p className="mt-3">{message}</p>}
      <form onSubmit={handleLogin}>
            <input type="email" name="email" placeholder="Email" value={formData.email}  onChange={handleChange} className="form-control mb-3"/>
            <input type="password" name="password" placeholder="Password" value={formData.password}  onChange={handleChange} className="form-control mb-3"/>
            <button type="submit" className="btn btn-success">Login</button>
      </form>
     
    </div>
  );
};

export default LoginPage;
