import React from "react";
import Navbar from "./components/Navbar";
import Main from "./components/Main";
function App() {
  return (
    <div className="overflow-auto scroll-smooth scrollbar-hide">
      <Navbar />
      <Main />
    </div>
  );
}

export default App;
