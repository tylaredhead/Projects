import React, { useEffect, useState } from 'react';
import { RegisterUser, encryptData } from '../../LoginUser.js';
import DropdownMenu from '../DropdownMenu.jsx';
import './Login.css';

// add encryption to password and username in session storage
function Register() {
    const [username, setusername] = useState("");
    const [password, setpassword] = useState("");
    const [role, setrole] = useState("");
    const [error, seterror] = useState(false);
    const [showToggle, setshowToggle] = useState(false);

    const updateusername = (s) => {setusername(s.target.value);};
    const updatepassword = (s) => {setpassword(s.target.value);};
    const handleToggle = () => {setshowToggle(!showToggle);};

    const login = JSON.parse(localStorage.getItem('login'));
//everything centred, check not default values, add validation
    const handleRegisterAuth = async (e) => {
        e.preventDefault();
        try {
            //const data = await encryptData({'username':username, password:password});
            console.log(password);
            const token = await RegisterUser({
                'username':login.username,
                'password':login.password, 
                'newUsername':username, 
                'newPassword':password,
                'role':role
            });

            console.log(token);

            if (token.msg === 'OK') seterror(false);
            else seterror(true);
        } catch (err) {
            seterror(true);
        }
    };
    // add so msg only show on submission for set time
    return (
        <div className = 'loginPage'>
            <div className='container'>
                <h2>Register new user</h2>

                <form onSubmit={handleRegisterAuth}>                 
                    <label for='username'>Username:</label>
                    <input type='text' id='username' name='username' placeholder='Enter the username...' onChange={updateusername} required />
                    <label for='password'>Password:</label>
                    <div className='password-container'>
                        <input className='password-input' 
                            type={(showToggle) ? 'text' : 'password'} 
                            id='password' 
                            name='password' 
                            placeholder='Enter your password...' 
                            onChange={updatepassword} 
                            required 
                        />
                        <img 
                            src={(!showToggle) ? 'showToggle.svg' : 'hideToggle.svg'} 
                            alt='show toggle password' 
                            onClick={handleToggle} 
                        />
                    </div>
                    <label for='auth'>Authorisation level:</label>
                    <DropdownMenu options={['admin', 'employee', 'user']} saveId='AuthToken' getCurrTxt={(txt) => setrole(txt)} className='user-input'/>
                    <button className='button-events' type='submit'>Register</button>
                    
                    { error && <p className = 'error-msg'>
                        This has been unsuccessful. Try again!
                    </p>}
                    { !error && <p className = 'succ-msg'>
                        This has been successful
                    </p>}
                </form>
            </div>
        </div>
    );
}

export default Register;