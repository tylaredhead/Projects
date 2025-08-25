import React, { useLocation } from 'react';
import {Link} from 'react-router-dom';

import './navbar.css';

// deal with interactive elements, store username and password in session storage to verify each time and then type can't be misconfigured

function Navbar(){
    const handleLogOut = () => {<h1>Log out</h1>;
        // reset ENUM autheicate code and redirect to login page
    }

    const location = useLocation();
    const findActive = {
        'Get': (location.pathname === '/Get') ? 'active' : '',
        'Update': (location.pathname === '/Update') ? 'active' : '',
        'Delete': (location.pathname === '/Delete') ? 'active' : ''
    };

    // sort so can press anywhere on the box to naviagate
    // understand async and await

    return (
        <>
            <nav className='navbar'>
                <div className='navbar-container'>
                    <ul className='nav-links'>
                        <li><Link to='/Get' className='link {findActive.Get}'>Find</Link></li>
                        <li><Link to='/Update' className='link {findActive.Update'>Update</Link></li>
                        <li><Link to='/Delete'className='link {findActive.Delete}'>Delete</Link></li>
                        <li><Link to='/' className='link'>Log out</Link></li>
                    </ul>
                </div>
            </nav>
    </>
    );
}

export default Navbar;