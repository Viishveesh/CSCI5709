import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

// import pages 
import Login from "./pages/auth/Login";
import Signup from "./pages/auth/Signup";
import RequestLink from './pages/auth/RequestLink';
import ResetPassword from './pages/auth/ResetPassword';

// import css 
import "./assets/css/styles.css"

function App() {
  return(
     <Router>
      <div className="App">
        <Routes>
          {/* Public Routes */}
          <Route path="/login" element={<Login />} />
          <Route path="/request-reset" element={<RequestLink />} />
          <Route path="/reset-password" element={<ResetPassword />} />
          <Route path="/" element={<Signup />} />
          
        </Routes>
        {/* <Footer /> */}
      </div>
    </Router>
  )
}

export default App;