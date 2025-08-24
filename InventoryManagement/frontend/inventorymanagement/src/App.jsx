import React, { useState } from 'react';
import { BrowserRouter, Route, Routes } from 'react-router-dom';

import Login from './components/pages/Login';
import './App.css';


function AppContent() {
  //const location = useLocation();

  return (
    <>
      <h1> Login </h1>
    </>
  );
  
  /*return (
    <div>
        {location.pathname != '/' && <Navbar />}
        <Routes>
          <Route path='/' element={<Login />} />
          <Route path='/Get' element={<Get />} />
          <Route path='/Update' element={<Update />} />
          <Route path='/Delete' element={<Delete />} />
        </Routes>
    </div>
  );*/
}

function App() {
  return (
    <>
      <BrowserRouter>
        <Router>
          <AppContent />
        </Router>
      </BrowserRouter>
     
    </>
  );
}

export default App;
