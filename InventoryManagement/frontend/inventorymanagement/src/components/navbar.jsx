import React from 'react';
import { useLocation, Link } from 'react-router-dom';

import { LoginUser } from '../LoginUser.js';
import './navbar.css';

function Navbar(){
    const handleLogOut = () => {
        sessionStorage.removeItem('login');
    }

    const location = useLocation();
    const findActive = {
        'Get': (location.pathname === '/Get') ? 'active' : '',
        'Update': (location.pathname === '/Update') ? 'active' : '',
        'Delete': (location.pathname === '/Delete') ? 'active' : ''
    };

    const access = [true, false, false]
    const haveAccess = async (e) => {
        const token = await LoginUser({
            username: sessionStorage.getItem('login').username, 
            password: sessionStorage.getItem('login').password
        });
        // if location is update or delete)
    }
    // need user auth
    // do cards for items and get to see them, with shoppping 
    // employee/ admin roles - get post, delete, register user account 
    // cards to see items
    // add shopping cart
    // set up database with usernames and passwords

    return (
        <>
            <nav className='navbar'>
                <div className='navbar-container'>
                    <ul className='nav-links'>
                        <li className={findActive.Get}><Link to='/Get' className='link'>Find</Link></li>
                        <li className={findActive.Update}><Link to='/Update' className='link'>Update</Link></li>
                        <li className={findActive.Delete}><Link to='/Delete'className='link'>Delete</Link></li>
                        <li><Link to='/' className='link' onClick={handleLogOut}>Log out</Link></li>
                    </ul>
                </div>
            </nav>
    </>
    );
}

export default Navbar;