import { useState, useEffect } from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import NavBar from "./NavBar";
import SignUp from "./SignUp";
import Login from "./Login";

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  useEffect(() => {
    // Check if user is logged in
    fetch("/check_session")
      .then((r) => {
        if (r.ok) {
          setIsLoggedIn(true);
        }
      });
  }, []);

  return (
    <div>
      <Router>
        <NavBar />
        <div className="main-content">
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route path="/signup" element={<SignUp />} />
            <Route path="/" element={<Navigate to={isLoggedIn ? "/login" : "/signup"} />} />
          </Routes>
        </div>
      </Router>
    </div>    
  )
}

export default App;
