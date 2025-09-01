import React, { useEffect, useRef, useState } from 'react';
import { useLocation } from 'react-router-dom';
import { LoginUser } from '../../LoginUser.js';
import './Form.css';

import DropdownMenu from '../DropdownMenu.jsx';

export default function Get() {
    const location = useLocation();
    // id name  
    const option = sessionStorage.getItem('tableSelect');
    const login = JSON.parse(localStorage.getItem('login'));
    const [tblOptions, settblOptions] = useState([]);
    const [commandOptions, setCommandOptions] = useState([]);
    useEffect(() => {
        const haveAccess = async () => {
            const token = await LoginUser({
                username: login.username,
                password: login.password
            });

            switch (token.role){
                case ('admin') :
                    settblOptions(['Product', 'Supplier']);
                    setCommandOptions(['Get', 'Update', 'Delete']);
                    break;
                case ('employee') :
                    settblOptions(['Product', 'Supplier']);
                    setCommandOptions(['Get', 'Update']);
                    break;
                default:
                    settblOptions(['Product']);
                    setCommandOptions(['Get']);
            };
        };

        haveAccess();
    }, [login]);

    return (
        <div>
            <h1>Ammend Information</h1>
            <p>Select an option:</p>
            <DropdownMenu className='drop' options={tblOptions} saveId='tableSelect' />
            <DropdownMenu className='drop' saveId='pageSelect' options={commandOptions} />
            {(option === 'Product') && (<h2>HEllo</h2>)}
            {(option === 'Supplier') && (<h2>Boo</h2>)}
            
        </div>
    );
}