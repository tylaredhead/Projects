import React, { useState } from 'react';
import { BrowserRouter, Route, useLocation, Routes } from 'react-router-dom';

import Login from './components/pages/Login.jsx';
import Get from './components/pages/Get.jsx';
import Update from './components/pages/Update.jsx';
import Delete from './components/pages/Delete.jsx';
import Navbar from './components/Navbar.jsx';
import './App.css';


function AppContent() {
  const location = useLocation();
  
  return (
    <div>
        {location.pathname != '/' && <Navbar />}
        <Routes>
          <Route path='/' element={<Login />} />
          <Route path='/Get' element={<Get />} />
          <Route path='/Update' element={<Update />} />
          <Route path='/Delete' element={<Delete />} />
        </Routes>
    </div>
  );
}

function App() {
  return (
    <>
      <BrowserRouter>
        <AppContent />
      </BrowserRouter>
    </>
  );
}

export default App;
