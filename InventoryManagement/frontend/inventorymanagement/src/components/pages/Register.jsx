import React, { useEffect, useState } from 'react';
import { RegisterUser, encryptData } from '../../LoginUser.js';
import DropdownMenu from '../DropdownMenu.jsx';
import './Login.css';

// add encryption to password and username in session storage
function Register() {
    const [username, setusername] = useState("");
    const [password, setpassword] = useState("");
    const [role, setrole] = useState("");
    const [error, seterror] = useState(0);
    const [showToggle, setshowToggle] = useState(false);

    const updateusername = (s) => {
        setusername(s.target.value);
        seterror(0);
    };
    const updatepassword = (s) => {
        setpassword(s.target.value);
        seterror(0);
    };
    const handleToggle = () => {setshowToggle(!showToggle);};

    const login = JSON.parse(localStorage.getItem('login'));
//everything centred, check not default values, add validation
    const handleRegisterAuth = async (e) => {
        e.preventDefault();
        try {
            if (role === "Choose an option...") seterror(2);
            else {
                //const data = await encryptData({'username':username, password:password});
                const token = await RegisterUser({
                    'username':login.username,
                    'password':login.password, 
                    'newUsername':username, 
                    'newPassword':password,
                    'role':role
                });
                if (token.msg === 'OK') {
                    seterror(1);
                    setusername("");
                    setpassword("");
                    setrole("Choose an option...");
                } else seterror(2);

            }
        } catch (err) {
            seterror(2);
        }
    };
    // add so msg only show on submission for set time
    return (
        <div className = 'loginPage'>
            <div className='container'>
                <h2>Register new user</h2>

                <form onSubmit={handleRegisterAuth}>                 
                    <label for='username'>Username:</label>
                    <input type='text' id='username' name='username' placeholder='Enter the username...' onChange={updateusername} value={username} required />
                    <label for='password'>Password:</label>
                    <div className='password-container'>
                        <input className='password-input' 
                            type={(showToggle) ? 'text' : 'password'} 
                            id='password' 
                            name='password' 
                            placeholder='Enter your password...' 
                            onChange={updatepassword} 
                            value={password}
                            required 
                        />
                        <img 
                            src={(!showToggle) ? 'showToggle.svg' : 'hideToggle.svg'} 
                            alt='show toggle password' 
                            onClick={handleToggle} 
                        />
                    </div>
                    <label for='auth'>Authorisation level:</label>
                    <DropdownMenu 
                        options={['admin', 'employee', 'user']} 
                        value={role}
                        className='user-input'
                        getCurrTxt={(txt) => {
                            setrole(txt);
                            seterror(0);
                        }} 
                    />
                    <button className='button-events' type='submit'>Register</button>
                    
                    {(error === 2) && <p className = 'error-msg'>
                        This has been unsuccessful. Try again!
                    </p>}
                    {(error === 1) && <p className = 'succ-msg'>
                        This has been successful.
                    </p>}
                </form>
            </div>
        </div>
    );
}

export default Register;