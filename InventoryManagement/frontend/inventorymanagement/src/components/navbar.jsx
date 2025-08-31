import React , { useEffect, useState } from 'react';
import { useLocation, Link } from 'react-router-dom';

import { LoginUser } from '../LoginUser.js';
import './navbar.css';

function Navbar(){
    const [access, setAccess] = useState([true, false, false]);
    const handleLogOut = () => {
        localStorage.removeItem('login');
    }

    const location = useLocation();
    const findActive = {
        'Get': (location.pathname === '/Get') ? 'active' : '',
        'Update': (location.pathname === '/Update') ? 'active' : '',
        'Delete': (location.pathname === '/Delete') ? 'active' : ''
    };

    //const access = [true, true, true];

    // [0] => Get page, [1] => Update page, [2] => Delete page
    const login = JSON.parse(localStorage.getItem('login'));
    useEffect(() => {
        const haveAccess = async () => {
            const token = await LoginUser({
                username: login.username, 
                password: login.password
            });

            if (token.role === 'admin') setAccess([true, true, true]);
            else if (token.role === 'employee') setAccess([true, true, false]);
            else setAccess([true, false, false]);
        }; 
        
        haveAccess();
    }, [login]);     
    
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
                        {access[0] === true && (<li className={findActive.Get}><Link to='/Get' className='link'>Find</Link></li>)}
                        {access[1] === true && (<li className={findActive.Update}><Link to='/Update' className='link'>Update</Link></li>)}
                        {access[2] === true && (<li className={findActive.Delete}><Link to='/Delete'className='link'>Delete</Link></li>)}
                        <li className={'fixed'}><Link to='/' className='link' onClick={handleLogOut}>Log out</Link></li>
                    </ul>
                </div>
            </nav>
    </>
    );
}

export default Navbar;