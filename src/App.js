import React from "react";
import Navbar from "./components/Navbar";
import Main from "./components/Main";



function App() {
  return (
    <div className="overflow-auto scroll-smooth scrollbar-hide">
      <Navbar />
      <div className="py-12 bg-black">
      <Main /> 
      </div>
    </div>
  );
}

export default App;
