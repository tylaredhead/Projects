import React from 'react';
import './navbar.css';
import {BrowserRouter as Router, Route, Routes, Link} from 'react-router-dom';

import Get from './pages/Get.jsx'; 
// deal with interactive elements

function Navbar(){
    const handleLogOut = () => {
        // reset ENUM autheicate code and redirect to login page
    }

    return (
        <>
            <Router>
                <nav className='navbar'>
                    <div className='navbar-container'>
                        <ul className='nav-links'>
                            <li><Link to='/Get'>Find</Link></li>
                            <li><a href='/Update'>Update</a></li>
                            <li><a href='/Delete'>Delete</a></li>
                            <li><a href='/Log out' onClick={handleLogOut}>Log out</a></li>
                        </ul>
                    </div>
                </nav>
                <Routes>
                    <Route path="/Get" element={<Get />} />
                </Routes>
            </Router>
        </>
    );
}

export default Navbar;