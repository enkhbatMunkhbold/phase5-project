// import { useEffect, useState } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import NavBar from "./NavBar";

function App() {
  return (
    <div>
      <Router>
        <NavBar />
      </Router>
    </div>    
  )
}

export default App;
