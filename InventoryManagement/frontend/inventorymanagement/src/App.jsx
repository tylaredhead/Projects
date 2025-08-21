import React, { useState } from 'react';
import reactLogo from './assets/react.svg';
import { BrowserRouter as Router, Route, useLocation, Routes } from 'react-router-dom';
import viteLogo from '/vite.svg';

import Login from './components/pages/Login';
import './App.css';


function App() {
  return (
    <>
      <Login />
    </>
  )
}

export default App
