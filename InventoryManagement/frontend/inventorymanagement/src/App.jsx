import React, { useState } from 'react';
import { BrowserRouter as Router, Route, useLocation, Routes } from 'react-router-dom';
import viteLogo from '/vite.svg';

import Login from './components/pages/Login';
import Navbar from './components/navbar';
import Get from './components/pages/Get';
import Update from './components/pages/Update'; 
import Delete from './components/pages/Delete';
import './App.css';


function App() {
  const location = useLocation();
  
  return (
    <div>
      <Router>
        <Login />
        (location.pathname != '/' && {<Navbar />});
        <Routes>
          <Route path='/' element={<Login />} />
          <Route path='/Get' element={<Get />} />
          <Route path='/Update' element={<Update />} />
          <Route path='/Delete' element={<Delete />} />
        </Routes>
      </Router>
    </div>
  );
}

export default App;
