import React from 'react';
import { useLocation, Link } from 'react-router-dom';

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
    //alert(location.pathname);

    return (
        <>
            <nav className='navbar'>
                <div className='navbar-container'>
                    <ul className='nav-links'>
                        <li className={findActive.Get}><Link to='/Get' className='link'>Find</Link></li>
                        <li className={findActive.Update}><Link to='/Update' className='link'>Update</Link></li>
                        <li className={findActive.Delete}><Link to='/Delete'className='link'>Delete</Link></li>
                        <li><Link to='/' className='link'>Log out</Link></li>
                    </ul>
                </div>
            </nav>
    </>
    );
}

export default Navbar;