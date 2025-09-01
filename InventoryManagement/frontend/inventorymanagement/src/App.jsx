import React from 'react';
import { BrowserRouter, Route, useLocation, Routes } from 'react-router-dom';

import Login from './components/pages/Login.jsx';
import Get from './components/pages/Get.jsx';
import Update from './components/pages/Update.jsx';
import Register from './components/pages/Register.jsx';
import Navbar from './components/navbar.jsx';
import Footer from './components/Footer.jsx';
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
          <Route path='/Register' element={<Register />} />
        </Routes>
        <Footer />
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
