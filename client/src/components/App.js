import { useState, useEffect } from "react";
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
      <NavBar />
      <div className="main-content">
        {!isLoggedIn ? (
          <SignUp />
        ) : (
          <Login />
        )}
      </div>
    </div>    
  )
}

export default App;
