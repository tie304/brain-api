import React, {useContext, useEffect} from 'react';
import './App.css';
import Header from "./components/Header"
import Router from "./components/Router";


const App = () => {
  return (
      <div>
          <Header/>
          <Router />
       </div>
      )
}

export default App;
