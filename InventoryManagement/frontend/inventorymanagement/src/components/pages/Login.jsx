import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { LoginUser } from '../../LoginUser.js';
import './Login.css';

function Login() {
    const [username, setusername] = useState("");
    const [password, setpassword] = useState("");
    const [invalidLogin, setinvalidLogin] = useState(false);
    const [showToggle, setshowToggle] = useState(false);
    const [isLoading, setisLoading] = useState(false);

    const updateusername = (s) => {setusername(s.target.value);};
    const updatepassword = (s) => {setpassword(s.target.value);};
    const handleToggle = () => {setshowToggle(!showToggle);};

    const handleLoginAuth = () => {
        try {
            const token = LoginUser({username:username, password:password});
            if (token.role === 'admin') {
                setinvalidLogin(false);
                navigate('/Get');
            } else setinvalidLogin(true);
        } catch (error) {
            setinvalidLogin(true);
        }
    };

    const navigate = useNavigate();

    // need a condiitonal that sends token and if false add p, sort rerendering on conditional, eye for pass and loading on submit button
    return (
        <div className = 'loginPage'>
            <div className='container'>
                <h1>Login</h1>

                
                <form onSubmit={handleLoginAuth}>                 
                    <label for='username'>Username:</label>
                    <input type='text' id='username' name='username' placeholder='Enter your username...' onChange={updateusername} required />
                    <label for='password'>Password:</label>
                    <div className='password-container'>
                        <input className='password-input' type={(showToggle) ? 'text' : 'password'} id='password' name='password' placeholder='Enter your password...' onChange={updatepassword} required />
                        <img src={(!showToggle) ? '/public/showToggle.svg' : '/public/hideToggle.svg'} alt='show toggle password' onClick={handleToggle}></img>
                    </div>
                    <button className='button-events' type='submit'>
                        Log in
                    </button>
                    { invalidLogin && <p className = 'error-msg'>Your username or password entered is invalid, try again!</p>}
                    <p>Can't login? Contact admin for an account</p>
                </form>
            </div>
        </div>
    );
}

export default Login;